import django_filters as filters
from . import models


class StaffFilter(filters.FilterSet):

    name = filters.CharFilter("name", lookup_expr="contains", label="الإسم")

    class Meta:
        model = models.Staff
        fields = [
            "name",
            "faculty",
            "specialty",
            "degree",
            "time",
            "is_local",
            "is_countable",
        ]
