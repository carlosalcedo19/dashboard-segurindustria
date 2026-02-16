from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
from django.urls import path
from django.shortcuts import render
from apps.base.admin import BaseAdmin
from apps.crm.choices import LeadStatusChoices
from apps.crm.models import Lead
from django.urls import path
from django.db.models import Q
from apps.users.models import User
from apps.maintenance.models import Fair
from django.db import models
from django.contrib.admin import SimpleListFilter
from django.utils import timezone


class SubordinatesFilter(SimpleListFilter):
    title = 'Asesor' 
    parameter_name = 'agent'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            users = User.objects.all()
        else:
            users = User.objects.filter(
                models.Q(id=request.user.id) | models.Q(boss=request.user)
            )
        return [(u.id, str(u)) for u in users]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(creator_user_id=self.value())
        return queryset

class LeadAdmin(BaseAdmin):
    list_display = ('client', 'channel', 'product', 'amount','date', 'status_color', 'edit',)
    search_fields = ('client__name',) 
    list_filter = ('status', 'channel', 'date',SubordinatesFilter,)
    exclude = ['is_active', 'state', 'creator_user',]
    filter_horizontal = ('product_lines',)
    list_display_links = ['edit', 'client']

    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='crm_lead_dashboard'),
        ]
        return custom_urls + urls

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "agent":
                kwargs["queryset"] = User.objects.filter(
                    Q(id=request.user.id) | Q(boss=request.user)
                ).distinct()
            
            if db_field.name == "fair":
                hoy = timezone.now().date()
                feria_qs = Fair.objects.filter(start_date__lte=hoy, end_date__gte=hoy)
                if not feria_qs.exists():
                    feria_qs = Fair.objects.order_by('-created_at')[:1]
                kwargs["queryset"] = feria_qs
                
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial['agent'] = request.user.id
        
        hoy = timezone.now().date()
        feria_actual = Fair.objects.filter(start_date__lte=hoy, end_date__gte=hoy).first()
        if not feria_actual:
            feria_actual = Fair.objects.order_by('-created_at').first()
            
        if feria_actual:
            initial['fair'] = feria_actual.id
        return initial

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            is_boss = User.objects.filter(boss=request.user).exists()
            if not is_boss:
                obj.agent = request.user
            
            if not change or not obj.fair:
                hoy = timezone.now().date()
                feria_actual = Fair.objects.filter(start_date__lte=hoy, end_date__gte=hoy).first()
                if not feria_actual:
                    feria_actual = Fair.objects.order_by('-created_at').first()
                obj.fair = feria_actual

        if obj.fair:
            obj.amount = None
            obj.reason = None
            obj.product = None

        if obj.channel and obj.channel.channel_type == "digital":
            obj.fair = None

        super().save_model(request, obj, form, change)


    
    
    
    def dashboard_view(self, request):
        context = {
            **self.admin_site.each_context(request),
            "title": "Dashboard de Ventas Real-Time",
        }
        return render(request, "admin/dashboard_crm.html", context)
    
    def status_color(self, obj):
        paleta = {
            LeadStatusChoices.NV: {"bg": "#dbebff", "text": "#2b36d4", "border": "#ffffff"}, 
            LeadStatusChoices.EC: {"bg": "#f5f3ff", "text": "#7c3aed", "border": "#ede9fe"},
            LeadStatusChoices.CO: {"bg": "#fff7ed", "text": "#ea580c", "border": "#ffedd5"}, 
            LeadStatusChoices.VE: {"bg": "#f0fdf4", "text": "#15803d", "border": "#dcfce7"}, 
            LeadStatusChoices.PE: {"bg": "#ffe7e7", "text": "#dc2626", "border": "#fddada"}, 
        }
        
        config = paleta.get(obj.status, {"bg": "#f9fafb", "text": "#4b5563", "border": "#f3f4f6"})
        
        return format_html(
            '<span style="background-color: {}; color: {}; border: 1px solid {}; padding: 2px 10px; border-radius: 6px; font-size: 10px; font-weight: 500; text-transform: uppercase;">{}</span>',
            config["bg"],
            config["text"],
            config["border"],
            obj.get_status_display()
        )
    
    status_color.short_description ="Estado"

    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(
            Q(agent=request.user) | Q(agent__boss=request.user)
        ).distinct()
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if obj is not None:
            is_owner = obj.agent == request.user
            is_boss = obj.agent and obj.agent.boss == request.user
            
            if not (is_owner or is_boss):
                return False

        return super().has_change_permission(request, obj)

    
    class Media:
        js = ("admin/js/lead_dynamic_fields.js",)



admin.site.register(Lead, LeadAdmin)