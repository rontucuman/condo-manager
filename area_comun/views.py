import os

from django.shortcuts import render

from condomanager import settings
from condomanager.tools.AzureBlobManager import AzureBlobManager
from receipt.models import Receipt
from .forms import AreaComunForm, ReservaAreaComunForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.urls import reverse
from .models import AreaComun, User
from datetime import datetime
from django.db import IntegrityError

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
            form.instance.administrador = request.user
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

@login_required
def lista_areas_comunes(request):
    # Caso para multiples administradores
    # lista_areas_comunes = AreaComun.objects.filter(administrador=request.user).order_by("nombre")
    lista_areas_comunes = AreaComun.objects.all().order_by("nombre")
    return render(request, "lista_areas_comunes.html", {
        "lista_areas_comunes": lista_areas_comunes
    })

@login_required
def reservar_area_comun(request, area_comun_id):
    area_comun = AreaComun.objects.get(id=area_comun_id)
    
    if request.method == "POST":
        form = ReservaAreaComunForm(request.POST)
        if form.is_valid():
            form.instance.propietario = request.user
            form.instance.area_comun = area_comun
            if area_comun.costo == 0:
                form.instance.confirmada = True
            try:
                form.save()
                return HttpResponseRedirect(reverse("mis_reservas_area_comun"))                
            except IntegrityError:
                form.add_error("fecha", "Area comun no disponible en fecha: " + request.POST["fecha"])
        
        return render(request, "reservar_area_comun.html", { 
            "area_comun": area_comun, 
            "reserva_area_comun": form
        })
    return render(request, "reservar_area_comun.html", { "area_comun": area_comun, "reserva_area_comun": ReservaAreaComunForm()})

@login_required
def mis_reservas_area_comun(request):
    usuario = User.objects.get(username=request.user.username)
    mis_reservas = usuario.misReservas.all()
    return render(request, "mis_reservas_area_comun.html", { "mis_reservas": mis_reservas })


@login_required
def ver_recibo(request, reserva_id):

    receipts_path = os.path.join(settings.STATICFILES_DIRS[0], 'receipts/')
    if not os.path.exists(receipts_path):
        os.makedirs(receipts_path)

    if Receipt.objects.filter(reservation_id=reserva_id, is_canceled=False).count() > 0:
        receipt = Receipt.objects.get(reservation_id=reserva_id)
        receipt_filename = receipt.filename
        receipt_filepath = os.path.join(receipts_path, receipt_filename)
        if settings.ENVIRONMENT == 'production' and not os.path.exists(receipt_filepath):
            blob_manager = AzureBlobManager()
            blob_manager.download_file(filename=receipt_filename, dest_folder=receipts_path)

        if os.path.exists(receipt_filepath):
            return FileResponse(open(receipt_filepath, 'rb'), content_type='application/pdf', filename=receipt_filename)

    return HttpResponse("El recibo no fue encontrado")
