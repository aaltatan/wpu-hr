from django.utils.translation import gettext_lazy as _
import django_filters as filters
from . import models


class StaffFilter(filters.FilterSet):
    
    name = filters.CharFilter("name", lookup_expr="contains", label=_('Name'))
    faculty = filters.AllValuesFilter(
        'specialty__faculty__name', 
        lookup_expr="exact", 
        label=_('Faculty')
    )
    is_specialist = filters.BooleanFilter(
        'specialty__is_specialist',
        lookup_expr="exact",
        label=_('Is Specialist')
    )
    class Meta:
        model = models.Staff
        fields = [
            "name",
            "faculty",
            "specialty",
            "degree",
            "time",
            "is_specialist",
            "is_local",
            "is_countable",
        ]
