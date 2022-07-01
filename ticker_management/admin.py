from django.contrib import admin
from ticker_management.models import TickerDetails,TickerHistory

class AdminTable(admin.ModelAdmin):
    pass
admin.site.register(TickerDetails,AdminTable)
admin.site.register(TickerHistory,AdminTable)