from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
from apps.base.admin import BaseAdmin
from apps.maintenance.models import Channel, Product, ProductLine, Fair

class ChannelAdmin(BaseAdmin):
    list_display=('name','channel_type','description','edit',)
    list_filter= ('channel_type',)
    search_fields=('name',)
    exclude = ['is_active', 'state', 'creator_user',]
    list_display_links = ['edit','name']

    
    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'


class FairAdmin(BaseAdmin):
    list_display=('name', 'start_date','end_date','place','edit',)
    search_fields=('name',)
    exclude = ['is_active', 'state', 'creator_user',]
    list_display_links = ['edit','name']

    
    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'

class ProductAdmin(BaseAdmin):
    list_display=('name','productline','detail','edit',)
    search_fields=('name',)
    list_filter=('productline',)
    exclude = ['is_active', 'state', 'creator_user',]
    list_display_links = ['edit','place']

    
    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'


class ProductLineAdmin(BaseAdmin):
    list_display=('name','detail','edit',)
    search_fields=('name',)
    exclude = ['is_active', 'state', 'creator_user',]
    list_display_links = ['edit','place']

    
    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'



    
admin.site.register(Channel, ChannelAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductLine, ProductLineAdmin)
admin.site.register(Fair, FairAdmin)