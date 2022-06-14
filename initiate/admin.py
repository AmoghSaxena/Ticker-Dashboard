from django.contrib import admin
from initiate.models import TickerDetails,TickerHistory

# Register your models here.
class AdminTable(admin.ModelAdmin):
    pass
admin.site.register(TickerDetails,AdminTable)
admin.site.register(TickerHistory,AdminTable)