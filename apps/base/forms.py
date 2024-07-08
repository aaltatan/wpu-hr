from django import forms


CAPACITY_CHOICES = (
    ('new_with_supporters_percentage', 'new with supporters percentage'),
    ('new_without_supporters_percentage', 'new without supporters percentage'),
    ('old', 'old'),
)


class ResultsFilter(forms.Form):
  
    capacity = forms.ChoiceField(
      choices=CAPACITY_CHOICES, 
      label='Capacity', 
      required=False
    )
    local_include_masters = forms.BooleanField(
      label='include masters in local function', 
      initial=False, 
      required=False
    )
    