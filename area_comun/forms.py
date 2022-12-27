from django import forms
from .models import AreaComun, ReservaAreaComun
from datetime import datetime
from django.core.exceptions import ValidationError

def validate_date(date):
    if date < datetime.now().date():
        raise ValidationError("La fecha no puede estar en el pasado")

class AreaComunForm(forms.ModelForm):

    costo = forms.IntegerField(required=False)
    mobiliario = forms.CharField(max_length=100, required=False)

    class Meta:
        model = AreaComun
        fields = "__all__"
        # descomentar si se aplica mas de un administrador
        # exclude = ["administrador"]

class ReservaAreaComunForm(forms.ModelForm):
    class DateInput(forms.DateInput):
        input_type = "date"

    fecha = forms.DateField(widget=DateInput, initial=datetime.today, validators=[validate_date])
    class Meta:
        model = ReservaAreaComun
        fields = ["fecha"]

