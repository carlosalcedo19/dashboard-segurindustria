
from django.contrib import admin
from django.urls import path
from apps.crm.views import lead_stats_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/lead-stats/', lead_stats_api, name='lead_stats_api'),
]
