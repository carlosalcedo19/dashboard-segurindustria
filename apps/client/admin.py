from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
from django.db.models import Q
from apps.base.admin import BaseAdmin
from apps.client.models import Client, Company
from django.contrib.admin import SimpleListFilter
from apps.users.models import User
from django.db import models

class SubordinatesFilter(SimpleListFilter):
    title = 'Asesor' 
    parameter_name = 'creator_user'

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

class CompanyAdmin(BaseAdmin):
    list_display=('name','ruc','industry','edit',)
    search_fields=('name',)
    exclude = ['is_active', 'state', 'creator_user',]
    list_filter=(SubordinatesFilter,)
    list_display_links = ['edit','name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs

        return qs.filter(
            Q(creator_user=request.user) | Q(creator_user__boss=request.user)
        ).distinct()

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.creator_user != request.user:
            return False
        return super().has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.creator_user != request.user:
            return False
        return super().has_view_permission(request, obj)

    
    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'


class ClientAdmin(BaseAdmin):
    list_display=('document_number','first_name','last_name','email','phone','edit',)
    search_fields=('first_name','last_name')
    list_filter=(SubordinatesFilter,)
    exclude = ['is_active', 'state', 'creator_user',]
    list_display_links = ['edit','document_number']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs

        return qs.filter(
            Q(creator_user=request.user) | Q(creator_user__boss=request.user)
        ).distinct()

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.creator_user != request.user:
            return False
        return super().has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.creator_user != request.user:
            return False
        return super().has_view_permission(request, obj)


    class Media:
        js = ("admin/js/client_person_type.js",)

    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'

admin.site.register(Client, ClientAdmin)
admin.site.register(Company, CompanyAdmin)