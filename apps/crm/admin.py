from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
from django.urls import path
from django.shortcuts import render
from apps.base.admin import BaseAdmin
from apps.crm.choices import LeadStatusChoices
from apps.crm.models import Lead
from apps.maintenance.models import Channel
from django.urls import path
from django.http import JsonResponse
from django.core.exceptions import ValidationError


class LeadAdmin(BaseAdmin):
    list_display = ('client', 'channel', 'product', 'amount', 'status_color', 'edit',)
    search_fields = ('client__name',) 
    list_filter = ('status', 'channel', 'date')
    exclude = ['is_active', 'state', 'creator_user',]
    list_display_links = ['edit', 'client']

    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='crm_lead_dashboard'),
        ]
        return custom_urls + urls
    
    def get_changeform_initial_data(self, request):
            return {
                "agent": request.user.id
            }

    def dashboard_view(self, request):
        context = {
            **self.admin_site.each_context(request),
            "title": "Dashboard de Ventas Real-Time",
        }
        return render(request, "admin/dashboard_crm.html", context)
    
    def status_color(self, obj):
        paleta = {
            LeadStatusChoices.NV: {"bg": "#dbebff", "text": "#2b36d4", "border": "#ffffff"}, # Azul
            LeadStatusChoices.EC: {"bg": "#f5f3ff", "text": "#7c3aed", "border": "#ede9fe"}, # Morado
            LeadStatusChoices.CO: {"bg": "#fff7ed", "text": "#ea580c", "border": "#ffedd5"}, # Naranja
            LeadStatusChoices.VE: {"bg": "#f0fdf4", "text": "#15803d", "border": "#dcfce7"}, # Verde Éxito
            LeadStatusChoices.PE: {"bg": "#ffe7e7", "text": "#dc2626", "border": "#fddada"}, # Rojo
        }
        
        config = paleta.get(obj.status, {"bg": "#f9fafb", "text": "#4b5563", "border": "#f3f4f6"})
        
        return format_html(
            '<span style="background-color: {}; color: {}; border: 1px solid {}; padding: 2px 10px; border-radius: 6px; font-size: 10px; font-weight: 500; text-transform: uppercase;">{}</span>',
            config["bg"],
            config["text"],
            config["border"],
            obj.get_status_display()
        )

    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'


    def save_model(self, request, obj, form, change):
        if obj.fair:
            obj.amount = None
            obj.reason = None
            obj.product = None

        if obj.channel and obj.channel.channel_type == "digital":
            obj.fair = None

        super().save_model(request, obj, form, change)


    
    class Media:
        js = ("admin/js/lead_dynamic_fields.js",)



admin.site.register(Lead, LeadAdmin)