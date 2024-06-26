from django import forms
from . import models

class StaffForm(forms.ModelForm):

    class Meta:
        model = models.Staff
        fields = '__all__'
        exclude = ['is_countable', 'notes']