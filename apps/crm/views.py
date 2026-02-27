from django.http import JsonResponse
from django.db.models import Count, Q
from .models import Lead
from django.shortcuts import render, redirect
from .forms import ClientForm, LeadForm, CompanyForm
from django.views.generic import TemplateView
from django.contrib import admin
from .models import Fair, Channel
from apps.client.models import Company, Client
from django.utils import timezone
from django.db import transaction
from apps.client.choices import PersonTypeChoices

def lead_stats_api(request):
    try:
        leads_qs = Lead.objects.all()

        if not request.user.is_superuser:
            leads_qs = leads_qs.filter(
                Q(agent=request.user) | Q(agent__boss=request.user)
            )

        leads_qs = leads_qs.select_related(
            'client', 'channel', 'product', 'agent'
        ).prefetch_related('product_lines').order_by('-date')

        leads_list = []
        for l in leads_qs:
            lines_names = ", ".join([str(pl) for pl in l.product_lines.all()])
            
            leads_list.append({
                "id": str(l.id), # Útil si usas UUID
                "date": l.date.strftime('%Y-%m-%d') if l.date else "-",
                "client": str(l.client) if l.client else "Sin Cliente",
                "client_type": l.client.get_person_type_display() if l.client else "N/A",
                "channel": str(l.channel) if l.channel else "Directo",
                "agent": str(l.agent) if l.agent else "No asignado",
                "product": (
                    str(l.product) if l.product 
                    else lines_names if lines_names 
                    else "N/A"
                ),
                "status": l.status,
                "amount": float(l.amount) if l.amount else 0.0,
                "reason": l.reason or "-"
            })

        reasons_qs = leads_qs.filter(status='Perdido')\
            .values('reason')\
            .annotate(value=Count('id'))
        
        reasons_data = [
            {"name": r['reason'] or "Otro/No especificado", "value": r['value']} 
            for r in reasons_qs
        ]

        channels_qs = leads_qs.values('channel__name').annotate(
            total=Count('id')
        ).order_by('-total')
        
        temp_channels = {}
        for c in channels_qs:
            name = (c['channel__name'] or "Otros").strip().upper() 
            temp_channels[name] = temp_channels.get(name, 0) + c['total']

        channels_data = [
            {"name": name, "value": value} 
            for name, value in temp_channels.items()
        ]
        return JsonResponse({
            "leads": leads_list,
            "reasons_data": reasons_data,
            "channels_data": channels_data,
        }, safe=False)

    except Exception as e:
        print(f"--- ERROR CRITICAL EN API DASHBOARD: {e} ---")
        return JsonResponse({"error": str(e)}, status=500)
 

class CreateLeadCustomView(TemplateView):
    template_name = "admin/custom_create_lead.html"

    def get_active_fairs(self):
        hoy = timezone.now().date()
        return Fair.objects.filter(
            start_date__lte=hoy,
            end_date__gte=hoy
        ).order_by('start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_fairs = self.get_active_fairs()
        selected_fair_id = self.request.GET.get("fair")
        
        canal_stand = Channel.objects.filter(name__icontains="STAND").first()
        context["active_fairs"] = active_fairs
        context["show_fair_selector"] = active_fairs.count() > 1 and not selected_fair_id
        
        initial = {"agent": self.request.user.id}
        if canal_stand: initial["channel"] = canal_stand.id
        if selected_fair_id: initial["fair"] = selected_fair_id
        elif active_fairs.count() == 1: initial["fair"] = active_fairs.first().id

        context.update({
            "lead_form": LeadForm(initial=initial),
            "client_form": ClientForm(),
            "company_form": CompanyForm(),
            **admin.site.each_context(self.request),
            "title": "Registro de Lead para Feria",
        })
        return context

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and 'check_duplicate' in request.POST:
            doc_num = request.POST.get('document_number')
            if doc_num:
                cliente = Client.objects.filter(document_number=doc_num).first()
                if cliente:
                    return JsonResponse({
                        'status': 'exists', 
                        'name': f"{cliente.first_name} {cliente.last_name}", 
                        'id': cliente.id
                    })
            return JsonResponse({'status': 'ok'})

        
        client_form = ClientForm(request.POST)
        lead_form = LeadForm(request.POST)
        company_form = CompanyForm(request.POST)

        existing_client_id = request.POST.get('existing_client_id')
        person_type_sent = request.POST.get('person_type')
        
        es_empresa = person_type_sent == 'Empresa'

        valid_client = True if (existing_client_id and existing_client_id != "new") else client_form.is_valid()
        valid_lead = lead_form.is_valid()
        
        target_company = None
        if es_empresa:
            ruc = request.POST.get('ruc')
            target_company = Company.objects.filter(ruc=ruc).first()
            
            if target_company:
                valid_company = True
            else:
                valid_company = company_form.is_valid()
        else:
            valid_company = True


        if valid_client and valid_lead and valid_company:
            try:
                with transaction.atomic():
                    if es_empresa and not target_company:
                        target_company = company_form.save()

                    if existing_client_id and existing_client_id != "new":
                        client = Client.objects.get(id=existing_client_id)
                    else:
                        client = client_form.save(commit=False)

                    if es_empresa:
                        client.person_type = 'Empresa'
                        client.company = target_company 
                        client.position = request.POST.get('position')
                    else:
                        client.person_type = 'Natural'
                        client.company = None
                    
                    client.save()

                    lead = lead_form.save(commit=False)
                    lead.client = client
                    if not lead.agent:
                        lead.agent = request.user
                    lead.save()
                    lead_form.save_m2m()
                    

                return redirect("admin:crm_lead_changelist")
                
            except Exception as e:
                print(f"DEBUG ERROR CRÍTICO EN TRANSACCIÓN: {e}")
        else:
            print("DEBUG: Error de validación, recargando formulario.")

        context = self.get_context_data(
            client_form=client_form, 
            lead_form=lead_form, 
            company_form=company_form
        )
        return self.render_to_response(context)