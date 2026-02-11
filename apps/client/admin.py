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

    
    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'


class ClientAdmin(BaseAdmin):
    list_display=('document_number','first_name','last_name','email','phone','edit',)
    search_fields=('first_name','last_name')
    exclude = ['is_active', 'state', 'creator_user',]
    list_display_links = ['edit','document_number']

    class Media:
        js = ("admin/js/client_person_type.js",)

    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'

admin.site.register(Client, ClientAdmin)
admin.site.register(Company, CompanyAdmin)