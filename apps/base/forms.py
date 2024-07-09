from django import forms
from django.utils.translation import gettext_lazy as _
from ..faculties.models import rate_validator


CAPACITY_CHOICES = (
    (
      'respect_each_specialty_fulltime_parttime_percentage', 
      _('respect EACH specialty f/p percentage'),
    ),
    (
      'calculate_all_specialties_as_one', 
      _('calculate ALL specialties as one'),
    ),
    (
      'respect_specialist_supporters_percentage', 
      _('respect specialist supporters percentage'), 
    ),
)
DEFAULT_LOCAL_PERCENTAGE: int = 50


class ResultsFilter(forms.Form):
  
    capacity = forms.ChoiceField(
      choices=CAPACITY_CHOICES, 
      label=_('capacity'), 
      required=False,
      help_text=_('capacity\'s calculation options'),
    )
    
    local_include_masters = forms.BooleanField(
      label=_('include masters in local calculation'), 
      initial=False, 
      required=False,
      help_text=_('include masters in local calculation'),
    )
    
    minimum_local_percentage = forms.IntegerField(
      label=_('minimum local percentage'),
      initial=DEFAULT_LOCAL_PERCENTAGE,
      required=False,
      help_text=_('minimum local percentage which ministry require'),
      validators=rate_validator,
    )