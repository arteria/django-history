from django.contrib import admin
 
from .models import *


class HistoryEventAdmin(admin.ModelAdmin):
    date_hierarchy = 'event_timestamp'
    list_display = ('content_type', 'event_timestamp', 'publish_timestamp', 'object_id')
    search_fields = ['content_type', 'slug', 'desc']
    list_filter = ('content_type', 'is_internal', 'is_hidden')


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('owner', )


admin.site.register(HistoryEvent, HistoryEventAdmin)    
admin.site.register(History, HistoryAdmin)
