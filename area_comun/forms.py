from django import forms
from .models import AreaComun

class AreaComunForm(forms.ModelForm):

    costo = forms.IntegerField(required=False)
    mobiliario = forms.CharField(max_length=100, required=False)

    class Meta:
        model = AreaComun
        fields = "__all__"