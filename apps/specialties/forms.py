from django import forms
from . import models



class SpecialtyForm(forms.ModelForm):
    
    class Meta:
        model = models.Specialty
        fields = '__all__'
