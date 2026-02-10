from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
from apps.base.admin import BaseAdmin
from apps.client.models import Client

class ClientAdmin(BaseAdmin):
    list_display=('document_number','full_name','email','phone','edit',)
    search_fields=('full_name',)
    exclude = ['is_active', 'state', 'creator_user',]
    list_display_links = ['edit','document_number']

    
    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'

admin.site.register(Client, ClientAdmin)