from django.contrib import admin
 
from history.models import *


class HistoryEventAdmin(admin.ModelAdmin):
    pass 


class HistoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(HistoryEvent, HistoryEventAdmin)    
admin.site.register(History, HistoryAdmin)
