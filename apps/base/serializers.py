from . import models
from rest_framework import serializers
from ..staff import serializers as staff_serializers


class FacultySerializer(serializers.ModelSerializer):

    staff = staff_serializers.StaffSerializer(many=True)
    class Meta:
        model = models.Faculty
        fields = [
            "name",
            "count_of_scholarship_students",
            "count_of_graduates",
            "count_of_students",
            "count_of_new_students",
            "ratio",
            "ratio_specialist_support",
            "ratio_count",
            "ratio_staff_count",
            'staff',
        ]