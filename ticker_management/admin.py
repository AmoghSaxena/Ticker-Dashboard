from django.contrib import admin
from ticker_management.models import TickerDetails,TickerHistory,SetUp

class AdminTable(admin.ModelAdmin):
    pass
admin.site.register(TickerDetails,AdminTable)
admin.site.register(TickerHistory,AdminTable)
admin.site.register(SetUp,AdminTable)