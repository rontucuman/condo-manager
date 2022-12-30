import datetime
import os
import uuid

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from xhtml2pdf import pisa

from area_comun.models import ReservaAreaComun
from condomanager.email.SingleAzureEmailSender import SingleAzureEmailSender
from condomanager.tools.AzureBlobManager import AzureBlobManager
from receipt.Reservation import Reservation
from receipt.models import Receipt


# Create your views here.

@login_required
def show_pdf(request, doc='none'):
    filename = doc
    path = os.path.join(settings.STATICFILES_DIRS[0], 'receipts/')
    filepath = os.path.join(path, filename)

    if settings.ENVIRONMENT == 'production' and not os.path.exists(filepath):
        blob_manager = AzureBlobManager()
        blob_manager.download_file(filename=filename, dest_folder=path)

    if os.path.exists(filepath):
        return FileResponse(open(filepath, 'rb'), content_type='application/pdf', filename=filename)

    return HttpResponse("El recibo no fue encontrado")


@login_required
def list_reservations(request):
    data = []
    reservations = ReservaAreaComun.objects.all()
    for rsv in reservations:
        reservation = Reservation()

        if Receipt.objects.filter(reservation_id=rsv.id).count() > 0:
            receipt = Receipt.objects.filter(reservation_id=rsv.id).first()
            reservation.reservation_id = receipt.reservation_id
            reservation.is_canceled = receipt.is_canceled
            reservation.receipt_id = receipt.id
            reservation.is_confirmed = receipt.is_reservation_confirmed
            reservation.user_id = receipt.user_id
            reservation.username = receipt.user.username
            reservation.common_area_id = receipt.common_area_id
            reservation.common_area_name = receipt.common_area.nombre
            reservation.begin_reservation_date = receipt.begin_reservation_date.date()
            reservation.end_reservation_date = receipt.end_reservation_date
            reservation.amount = receipt.reservation_amount
            reservation.receipt_filename = receipt.filename

        else:
            reservation.reservation_id = rsv.id
            reservation.is_canceled = False
            reservation.receipt_id = 0
            reservation.is_confirmed = rsv.confirmada
            reservation.user_id = rsv.propietario_id
            reservation.username = rsv.propietario.username
            reservation.common_area_id = rsv.area_comun_id
            reservation.common_area_name = rsv.area_comun.nombre
            reservation.begin_reservation_date = rsv.fecha
            reservation.end_reservation_date = rsv.fecha
            reservation.amount = '{:.2f}'.format(rsv.area_comun.costo)
            reservation.receipt_filename = 'not found'

        data.append(reservation)

    return render(request, 'list_reservations.html', {'reservations': data})


@login_required
def confirm_reservation(request):
    if request.method == 'POST':
        try:
            reservation_id = request.POST['reservation_id']
            rsv = ReservaAreaComun.objects.filter(id=reservation_id).first()
            rsv.confirmada = True
            rsv.save()
            receipt = Receipt()
            receipt.reservation_id = rsv.id
            receipt.user_id = rsv.propietario_id
            receipt.common_area_id = rsv.area_comun_id

            if Receipt.objects.count() == 0:
                receipt.receipt_number = 1
            else:
                receipt.receipt_number = Receipt.objects.latest('receipt_number').receipt_number + 1

            receipt.registered_date = datetime.datetime.now()
            receipt.is_canceled = False
            receipt.is_reservation_confirmed = True
            receipt.begin_reservation_date = rsv.fecha
            receipt.is_reservation_canceled = False
            receipt.reservation_amount = rsv.area_comun.costo
            receipt.paid_amount = rsv.area_comun.costo
            filename = generate_pdf(request, receipt)
            receipt.filename = filename
            receipt.save()
            send_email('confirm_reservation', receipt, filename)
            return HttpResponse(filename)
        except:
            return HttpResponse("No se pudo confirmar reserva. Intentelo nuevamente.")

    else:
        return HttpResponse("No se pudo confirmar reserva. Intentelo nuevamente.")


@login_required
def cancel_reservation(request):
    if request.method == 'POST':
        try:
            reservation_id = request.POST['reservation_id']
            rsv = ReservaAreaComun.objects.filter(id=reservation_id).first()
            rsv.confirmada = False
            rsv.save()

            receipt = Receipt.objects.filter(reservation_id=reservation_id).first()
            receipt.is_canceled = True
            receipt.save()

            send_email(receipt.user, 'cancel_reservation', receipt)
            return HttpResponse(f"La reserva del area comun ha sido cancelada")
        except:
            return HttpResponse("No se pudo cancelar reserva. Intentelo nuevamente.")

    else:
        return HttpResponse("No se pudo cancelar reserva. Intentelo nuevamente.")


def send_email(command, receipt, filename=''):
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
                                        {'user': receipt.user, 'receipt': receipt})
        plain_message = strip_tags(html_message)
        mail_to = receipt.user.email
        email_sender = SingleAzureEmailSender()
        # print('path del archivo pdf')
        # print(filepath)
        # if os.path.exists(filepath):
        #     print('existe el archivo pdf')
        #     email_sender.send_message_attachment(
        #         subject=subject,
        #         content_plain=plain_message,
        #         content_html=html_message,
        #         mail_to=mail_to,
        #         filepath=filepath)
        # else:
        #     print('no existe el archivo pdf')
        email_sender.send_message(
                subject=subject,
                content_plain=plain_message,
                content_html=html_message,
                mail_to=mail_to)


def generate_pdf(request, receipt):
    filename = f'receipt_{uuid.uuid4()}.pdf'
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

    dest.close()

    if settings.ENVIRONMENT == 'production':
        blob_manager = AzureBlobManager()
        blob_manager.upload_file(filename=filename, src_folder=path, content_type='application/pdf')

    return filename
