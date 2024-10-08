from django.contrib import admin
from .models import Inflow


@admin.register(Inflow)
class InflowAdmin(admin.ModelAdmin):
    list_display = ('product', 'supplier', 'quantity', 'created_at')
    search_fields = ('product__title', 'supplier__name')
