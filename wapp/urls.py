
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
                "sha256_cert_fingerprints": ["C8:27:0F:95:04:49:DE:3D:32:38:DF:1E:B4:9F:04:79:B5:F4:07:E4:0B:0D:17:55:C3:1E:AE:41:DF:89:3A:20"]
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
