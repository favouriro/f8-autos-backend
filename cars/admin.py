from django.contrib import admin
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('year', 'make', 'model', 'price', 'condition', 'is_available')
    list_filter = ('condition', 'is_available')
    search_fields = ('make', 'model')
    