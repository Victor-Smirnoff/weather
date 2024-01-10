from django import forms
from weather.models import Locations


class LocationForm(forms.ModelForm):
    class Meta:
        model = Locations
        fields = []