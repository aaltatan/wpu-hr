from django import forms
from . import models

class StaffForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['specialty'].queryset = (
            self
            .fields['specialty']
            .queryset
            .select_related('faculty')
        )
    
    class Meta:
        model = models.Staff
        fields = '__all__'
        exclude = ['is_countable', 'notes']