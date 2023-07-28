from django.contrib import admin

from .models import CustomerLog


@admin.register(CustomerLog)
class CustomerLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_id', 'request_time']
    list_filter = ['request_time', ]
    search_fields = ['customer_id', ]