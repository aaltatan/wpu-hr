from django.contrib import admin
from . import models


@admin.register(models.Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "count_of_scholarship_students",
        "count_of_graduates",
        "count_of_students",
        "ratio",
        "ratio_specialist_support",
        "ratio_count",
        "ratio_staff_count",
    ]
    fields = [
        "name",
        (
            "count_of_scholarship_students",
            "count_of_graduates",
            "count_of_students",
        ),
        (
            "ratio",
            "ratio_specialist_support",
        ),
        (
            "ratio_count",
            "ratio_staff_count",
        ),
    ]
    ordering = ["name"]
