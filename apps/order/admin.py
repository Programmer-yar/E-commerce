from django.contrib import admin
from .models import Order, OrderItem

from django.urls import reverse
import datetime


def order_name(obj):
    return f'{obj.first_name} {obj.last_name}'

#defining column name
order_name.short_description = 'Name'

#defines the 'additional actions' for the actions tab
def admin_order_shipped(modeladmin, request, queryset):
    for order in queryset:
        order.shipped_date = datetime.datetime.now()
        order.status = 'shipped'
        order.save()

admin_order_shipped.short_description = 'Set shipped'

class OrderItemInline(admin.TabularInline):
    """shows items of one order inside order """
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    #columns to be displayed
    list_display = ['id', order_name, 'status', 'created_at']
    #adding different filters like datetime and shipment status etc
    list_filter = ['created_at', 'status']
    #search on the basis of name and address
    search_fields = ['first_name', 'address']
    inlines = [OrderItemInline]
    actions = [admin_order_shipped]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
