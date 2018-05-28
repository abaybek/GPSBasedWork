from django import forms
from .models import GpsData

class GpsDataForm(forms.ModelForm):
    class Meta:
        model = GpsData
        fields = ('name', 'email', 'data', )
