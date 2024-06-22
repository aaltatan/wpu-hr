from django import forms
from . import models


class FacultyForm(forms.ModelForm):

    class Meta:
        model = models.Faculty
        fields = '__all__'