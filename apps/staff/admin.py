from django.contrib import admin
from . import models


@admin.register(models.Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "faculty",
        "specialty",
        "degree",
        "time",
        "is_local",
        "is_countable",
    ]
    search_fields = ["name"]
    fields = [
        "name",
        "specialty",
        ("degree", "time"),
        ("is_local", "is_countable"),
    ]
    list_filter = [
        'specialty__faculty',
        'specialty',
        'degree',
        'time',
        'is_local',
        'is_countable',
    ]
    ordering = [
        'specialty',
        'degree',
        '-time',
        'is_local',
        'is_countable',
        'name'
    ]
    list_per_page = 10
    show_full_result_count = True

    @admin.display(description="get faculty")
    def faculty(self, obj: models.Staff):
        return obj.specialty.faculty.name
