from django import forms
from . import models



class FacultySupporterForm(forms.ModelForm):
    
    class Meta:
        model = models.FacultySupporter
        fields = '__all__'
