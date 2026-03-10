
from django.contrib import admin
from django.urls import path, include
from apps.crm.views import lead_stats_api, CreateLeadCustomView
from apps.client.views import get_company_by_ruc
from django.views.generic import RedirectView
from django.http import JsonResponse


def asset_links(request):
    data = [
        {
            "relation": ["delegate_permission/common.handle_all_urls"],
            "target": {
                "namespace": "android_app",
                "package_name": "com.onrender.dashboard_segurindustria.twa",
                "sha256_cert_fingerprints": ["B8:24:8E:59:EF:8E:15:09:E5:37:0D:95:39:CD:DA:3E:CB:9E:76:08:09:C6:64:C2:16:09:BC:29:38:DE:4B:81"]
            }
            }
    ]
    return JsonResponse(data, safe=False)

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/'), name='home'),
    path('.well-known/assetlinks.json', asset_links),
    path('admin/', admin.site.urls),
    path('api/lead-stats/', lead_stats_api, name='lead_stats_api'),
    path('api/get-company/', get_company_by_ruc, name='get_company_by_ruc'),
    path('quick-lead/', admin.site.admin_view(CreateLeadCustomView.as_view()), name='quick_lead'),
    path('', include('pwa.urls')),
]
