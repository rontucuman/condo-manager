from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from xhtml2pdf import pisa

from condomanager.email.SingleAzureEmailSender import SingleAzureEmailSender
from receipt.Reservation import Reservation

import os


# Create your views here.


@login_required
def list_reservations(request):
    reservations = []
    for i in range(10):
        reservation = Reservation()
        reservation.reservation_id = i
        reservation.is_canceled = False
        reservation.receipt_id = i
        reservation.is_confirmed = False
        reservation.user_id = i
        reservation.username = f"username_{i}"
        reservation.common_area_id = 1000 + i
        reservation.common_area_name = f"common area name {i}"
        reservation.begin_reservation_date = reservation.begin_reservation_date.day.__add__(i)
        reservation.end_reservation_date = reservation.end_reservation_date.day.__add__(i + 1)
        reservation.amount = 10 * i
        reservations.append(reservation)

    return render(request, 'list_reservations.html', {'reservations': reservations})


@login_required
def confirm_reservation(request):
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
            # reservation.amount = 10 * i
            # print("reserva confirmada " + reservation_id)
            # user = User.objects.filter(id=user_id).first()
            # user.is_active = is_checked
            # user.save()
            generate_pdf(request, reservation_id)
            send_email(request.user, 'confirm_reservation', reservation)
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


def send_email(user, operation, reservation):
    subject = ''
    template_name = ''

    if operation == 'cancel_reservation':
        subject = 'Reserva de Area Comun Cancelada'
        template_name = 'email/cancel_reservation.html'
    elif operation == 'confirm_reservation':
        subject = 'Reserva de Area Comun Confirmada'
        template_name = 'email/confirm_reservation.html'

    if subject != '':
        html_message = render_to_string(template_name, {'username': user.username, 'reservation': reservation})
        plain_message = strip_tags(html_message)
        mail_to = user.email
        email_sender = SingleAzureEmailSender()
        email_sender.send_message(
            subject=subject,
            content_plain=plain_message,
            content_html=html_message,
            mail_to=mail_to)


def generate_pdf(request, reservation_id):
    filename = f'test{reservation_id}.pdf'
    path = os.path.join(settings.STATICFILES_DIRS[0], 'receipts/')

    if not os.path.exists(path):
        os.makedirs(path)

    filepath = os.path.join(path, filename)
    dest = open(filepath, 'w+b')
    template = get_template('receipts/pdf_template.html')
    html = template.render()
    result = pisa.CreatePDF(
        html,
        dest=dest,
    )
    print(result.pathDocument)
    # return HttpResponse(result)
    pass
