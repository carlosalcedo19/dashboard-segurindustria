from django.http import JsonResponse
from apps.client.models import Company

def get_company_by_ruc(request):
    ruc = request.GET.get('ruc')

    if not ruc:
        return JsonResponse({'status': 'error'}, status=400)

    try:
        company = Company.objects.get(ruc=ruc)

        return JsonResponse({
            'status': 'found',
            'id': company.id,                
            'name': company.name,
            'industry': company.industry,
        })

    except Company.DoesNotExist:
        return JsonResponse({
            'status': 'not_found'
        })