
from django.contrib import admin
from django.urls import path, include
from apps.crm.views import lead_stats_api, CreateLeadCustomView
from apps.client.views import get_company_by_ruc
from django.views.generic import RedirectView


urlpatterns = [
    path('', RedirectView.as_base(url='/admin/'), name='home'),
    path('admin/', admin.site.urls),
    path('api/lead-stats/', lead_stats_api, name='lead_stats_api'),
    path('api/get-company/', get_company_by_ruc, name='get_company_by_ruc'),
    path('quick-lead/', admin.site.admin_view(CreateLeadCustomView.as_view()), name='quick_lead'),
    path('', include('pwa.urls')),
]
