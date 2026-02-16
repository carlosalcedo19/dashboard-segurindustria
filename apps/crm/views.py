from django.http import JsonResponse
from django.db.models import Count, Q
from .models import Lead

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