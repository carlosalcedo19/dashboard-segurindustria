from django.http import JsonResponse
from django.db.models import Count
from .models import Lead

def lead_stats_api(request):
    try:
        # Query base
        leads_qs = Lead.objects.select_related(
            'client', 'channel', 'product','product_line', 'agent'
        ).order_by('-date')

        # Filtro por usuario si no es superuser
        if not request.user.is_superuser:
            leads_qs = leads_qs.filter(agent=request.user)

        # Lista de leads
        leads_list = []
        for l in leads_qs:
            leads_list.append({
                "id": l.id,
                "date": l.date.strftime('%Y-%m-%d') if l.date else "-",
                "client": str(l.client) if l.client else "Sin Cliente",
                "channel": str(l.channel) if l.channel else "Directo",
                "agent": str(l.agent) if l.agent else "No asignado",
                "product": (
                    str(l.product)
                    if l.product
                    else str(l.product_line) if l.product_line
                    else "N/A"
                ),
                "status": l.status,
                "amount": float(l.amount) if l.amount else 0.0,
                "reason": l.reason or "-"
            })

        # Base para estadísticas: respeta el usuario
        stats_qs = Lead.objects.all()
        if not request.user.is_superuser:
            stats_qs = stats_qs.filter(agent=request.user)

        # Razones de leads perdidos
        reasons_qs = stats_qs.filter(status='Perdido')\
            .values('reason')\
            .annotate(value=Count('id'))
        reasons_data = [
            {"name": r['reason'] if r['reason'] else "Otro/No especificado", "value": r['value']} 
            for r in reasons_qs
        ]

        # Canales de los leads
        channels_qs = stats_qs.values('channel__name')\
            .annotate(value=Count('id'))
        channels_data = [
            {"name": c['channel__name'] if c['channel__name'] else "Otros", "value": c['value']} 
            for c in channels_qs
        ]

        return JsonResponse({
            "leads": leads_list,
            "reasons_data": reasons_data,
            "channels_data": channels_data,
        }, safe=False)

    except Exception as e:
        print(f"--- ERROR CRITICAL EN API DASHBOARD: {e} ---")
        return JsonResponse({"error": str(e)}, status=500)
