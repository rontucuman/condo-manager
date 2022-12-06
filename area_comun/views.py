from django.shortcuts import render
from .forms import AreaComunForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

@login_required
def registrar_area_comun(request):
    if request.method == "POST":
        form = AreaComunForm(request.POST)
        
        if form.is_valid():
            if(form.cleaned_data["costo"] == None):
                form.instance.costo = 0
            if(form.cleaned_data["mobiliario"] == ""):
                form.instance.mobiliario = "Ninguno"
            form.save()
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            return render(request, "registro_area_comun.html", {
                "area_comun_form": form
            })
    else:
        return render(request, "registro_area_comun.html", {
        "area_comun_form": AreaComunForm()
    })
   