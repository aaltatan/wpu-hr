from django.contrib import admin
from . import models


@admin.register(models.Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'faculty',
        'specialty',
        'degree',
        'time',
        'is_staff',
    ]
    ordering = ['name']
    search_fields = ['name']

    @admin.display(description='get faculty')
    def faculty(self, obj):
        return obj.faculty.name