from django.contrib import admin
from . import models


@admin.register(models.Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "count_of_scholarship_students",
        "count_of_graduates",
        "count_of_students",
        "local_staff_percentage",
        "student_to_teacher_count",
        "student_to_local_teacher_count",
    ]
    fields = [
        "name",
        (
            "count_of_scholarship_students",
            "count_of_graduates",
            "count_of_students",
        ),
        (
            "local_staff_percentage",
            "student_to_teacher_count",
            "student_to_local_teacher_count",
        ),
    ]
    ordering = ["name"]
