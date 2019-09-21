from django.contrib import admin

from .models import MultiparametricReading

class MultiparametricReadingAdmin(admin.ModelAdmin):
    model = MultiparametricReading
    list_display = [
        'user',
        'created_date',
        'heart_rate',
        'oxygen_saturation',
        'body_temperature'
    ]
    readonly_fields = ['created_date']

admin.site.register(MultiparametricReading, MultiparametricReadingAdmin)

