from django.contrib import admin
from ticker_management.models import TickerDetails,TickerHistory,SetUp,RundeckLog

class TickerDetail(admin.ModelAdmin):
    list_display = ('ticker_id', 'rundeckid', 'ticker_type', 'ticker_title', 'ticker_priority', 'ticker_start_time', 'ticker_end_time', 'frequency' ,'created_by')

class TickerHistorys(admin.ModelAdmin):
    list_display = ('ticker_id', 'rundeckid', 'ticker_type', 'ticker_title', 'ticker_priority', 'ticker_start_time', 'ticker_end_time', 'frequency' ,'created_by')

class SetUps(admin.ModelAdmin):
    list_display = ('FQDN', 'Rundeck_Api_Version', 'Rundeck_Start_Job', 'Rundeck_Stop_Job', 'Apache_server_url', 'Ticker_FQDN')

class RundeckLogs(admin.ModelAdmin):
    list_display = ('ticker_id', 'rundeck_id', 'ticker_title', 'time_interval', 'execution', 'tickerStatus', 'successfull_nodes', 'failed_nodes', 'tv_status', 'iPad_status')


class AdminTable(admin.ModelAdmin):
    pass

admin.site.register(TickerDetails,TickerDetail)
admin.site.register(TickerHistory,TickerHistorys)
admin.site.register(SetUp,SetUps)
admin.site.register(RundeckLog,RundeckLogs)
admin.site.site_url = "/ticker"