from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.FacultySupporter)
class FacultySupporterAdmin(admin.ModelAdmin):
    list_display = [
        'faculty',
        'name',
        'percentage',
    ]
    
    ordering = ['faculty']