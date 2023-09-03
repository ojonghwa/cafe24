from django.http import HttpResponse
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Order, OrderItem
import csv
import datetime


def export_to_csv(modeladmin, request, queryset):       #340
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'   #order.csv

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    
    for obj in queryset:    # Write data rows
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%Y-%m-%d')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'   #select option name


def order_pdf(obj):         #354
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
order_pdf.short_description = 'Invoice'


def order_detail(obj):      #347
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')



class OrderItemInline(admin.TabularInline):     #307
    model = OrderItem
    raw_id_fields = ['product']     #상품명 대신 id 표시



@admin.register(Order)      #307,342,348
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'fullname', 'address', 'mobile', 'paid', 'created', order_detail, order_pdf]  
    list_filter = ['user', 'fullname', 'paid', 'created']
    inlines = [OrderItemInline]
    actions = [export_to_csv]

