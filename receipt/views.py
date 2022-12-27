import datetime

from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from xhtml2pdf import pisa

from condomanager.email.SingleAzureEmailSender import SingleAzureEmailSender
from receipt.Reservation import Reservation
from receipt.models import Receipt
from area_comun.models import ReservaAreaComun

import os
import base64


# Create your views here.

@login_required
def show_pdf(request, pdf_id=0):
    if pdf_id <= 0:
        return HttpResponse("El recibo no fue encontrado")
    else:
        filename = f'receipt_{pdf_id}.pdf'
        path = os.path.join(settings.STATICFILES_DIRS[0], 'receipts/')
        filepath = os.path.join(path, filename)
        if os.path.exists(filepath):
            return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
        else:
            return HttpResponse("El recibo no fue encontrado")



@login_required
def list_reservations(request):
    data = []
    reservations = ReservaAreaComun.objects.all()
    for rsv in reservations:
        reservation = Reservation()
        reservation.reservation_id = rsv.id
        reservation.is_canceled = False
        reservation.receipt_id = 0
        reservation.is_confirmed = rsv.confirmada
        reservation.user_id = rsv.propietario_id
        reservation.username = rsv.propietario.username
        reservation.common_area_id = rsv.area_comun_id
        reservation.common_area_name = rsv.area_comun.nombre
        reservation.begin_reservation_date = rsv.fecha
        # reservation.end_reservation_date = rsv.fecha
        reservation.amount = rsv.area_comun.costo
        data.append(reservation)

    return render(request, 'list_reservations.html', {'reservations': data})


@login_required
def confirm_reservation(request):
    if request.method == 'POST':
        try:
            reservation_id = request.POST['reservation_id']
            rsv = ReservaAreaComun.objects.filter(id=reservation_id).first()
            rsv.confirmada = True
            # rsv.save()
            receipt = Receipt()
            receipt.reservation_id = rsv.id
            receipt.registered_date = datetime.datetime.now()
            receipt.amount = rsv.area_comun.costo
            receipt.user_id = rsv.propietario_id
            receipt.common_area_id = rsv.area_comun_id
            if Receipt.objects.count() == 0:
                receipt.receipt_number = 1
            else:
                receipt.receipt_number = Receipt.objects.latest('receipt_number').receipt_number + 1
            receipt.save()

            file_path = generate_pdf(request, receipt)
            send_email(receipt.user, 'confirm_reservation', receipt, file_path)
            return HttpResponse(f"La reserva del area comun ha sido confirmada")
        except:
            return HttpResponse("No se pudo confirmar reserva. Intentelo nuevamente.")

    else:
        return HttpResponse("No se pudo confirmar reserva. Intentelo nuevamente.")


@login_required
def cancel_reservation(request):
    if request.method == 'POST':
        try:
            reservation_id = request.POST['reservation_id']
            reservation = Reservation()
            reservation.reservation_id = reservation_id
            reservation.is_canceled = False
            reservation.receipt_id = reservation_id
            reservation.is_confirmed = False
            reservation.user_id = request.user.id
            reservation.username = request.user.username
            reservation.common_area_id = reservation_id
            reservation.common_area_name = f"common area name {reservation_id}"
            reservation.begin_reservation_date = reservation_id
            reservation.end_reservation_date = reservation_id
            # user = User.objects.filter(id=user_id).first()
            # user.is_active = is_checked
            # user.save()
            send_email(request.user, 'cancel_reservation', reservation)
            return HttpResponse(f"La reserva del area comun ha sido cancelada")
        except:
            return HttpResponse("No se pudo cancelar reserva. Intentelo nuevamente.")

    else:
        return HttpResponse("No se pudo cancelar reserva. Intentelo nuevamente.")


def send_email(user, command, receipt, filepath):
    subject = ''
    template_name = ''

    if command == 'cancel_reservation':
        subject = 'Reserva de Area Comun Cancelada'
        template_name = 'email/cancel_reservation.html'
    elif command == 'confirm_reservation':
        subject = 'Reserva de Area Comun Confirmada'
        template_name = 'email/confirm_reservation.html'

    if subject != '':
        html_message = render_to_string(template_name,
                                        {'user': user, 'receipt': receipt})
        plain_message = strip_tags(html_message)
        mail_to = user.email
        email_sender = SingleAzureEmailSender()

        if os.path.exists(filepath):
            email_sender.send_message_attachment(
                subject=subject,
                content_plain=plain_message,
                content_html=html_message,
                mail_to=mail_to,
                filepath=filepath)
        else:
            email_sender.send_message(
                subject=subject,
                content_plain=plain_message,
                content_html=html_message,
                mail_to=mail_to)


def generate_pdf(request, receipt):
    filename = f'receipt_{receipt.reservation_id}.pdf'
    path = os.path.join(settings.STATICFILES_DIRS[0], 'receipts/')

    if not os.path.exists(path):
        os.makedirs(path)

    filepath = os.path.join(path, filename)
    dest = open(filepath, 'w+b')
    template = get_template('receipts/pdf_template1.html')
    context = {
        'data': receipt,
        'user': request.user
    }
    html = template.render(context)
    result = pisa.CreatePDF(
        html,
        dest=dest,
    )

    return filepath
