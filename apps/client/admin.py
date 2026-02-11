from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
from apps.base.admin import BaseAdmin
from apps.client.models import Client, Company

class CompanyAdmin(BaseAdmin):
    list_display=('name','ruc','industry','edit',)
    search_fields=('name',)
    exclude = ['is_active', 'state', 'creator_user',]
    list_display_links = ['edit','name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(creator_user=request.user)

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
    exclude = ['is_active', 'state', 'creator_user',]
    list_display_links = ['edit','document_number']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(creator_user=request.user)

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