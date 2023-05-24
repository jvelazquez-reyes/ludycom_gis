from django.forms import ModelForm
from .models import GeoLocalizer

class GeoLocalizerForm(ModelForm):
    class Meta:
        model = GeoLocalizer
        fields = ['latitude', 'longitude']