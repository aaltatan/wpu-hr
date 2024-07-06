from django.contrib import admin
from . import models


@admin.register(models.Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = [
        'faculty',
        'name',
        'percentage',
        'is_specialist',
    ]
    
    ordering = ['faculty']