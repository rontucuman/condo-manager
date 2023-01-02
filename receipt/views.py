from datetime import datetime
import os
import uuid

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from xhtml2pdf import pisa
from django.contrib.auth.models import User, Group

from area_comun.models import ReservaAreaComun, AreaComun
from condomanager.email.SingleAzureEmailSender import SingleAzureEmailSender
from condomanager.tools.AzureBlobManager import AzureBlobManager
from receipt.CustomFilters import CustomFilters
from receipt.Reservation import Reservation
from receipt.models import Receipt


# Create your views here.

@login_required
def show_pdf(request, doc='none'):
    receipt_filename = doc
    receipts_path = os.path.join(settings.STATICFILES_DIRS[0], 'receipts/')
    receipt_filepath = os.path.join(receipts_path, receipt_filename)

    if not os.path.exists(receipts_path):
        os.makedirs(receipts_path)

    if settings.ENVIRONMENT == 'production' and not os.path.exists(receipt_filepath):
        blob_manager = AzureBlobManager()
        blob_manager.download_file(filename=receipt_filename, dest_folder=receipts_path)

    if os.path.exists(receipt_filepath):
        return FileResponse(open(receipt_filepath, 'rb'), content_type='application/pdf', filename=receipt_filename)

    return HttpResponse("El recibo no fue encontrado")


@login_required
def list_reservations3(request, page=1, numitems=10):
    if not numitems.isnumeric():
        numitems = 10
    if not page.isnumeric():
        page = 1

    data = get_reservations()

    if request.method == 'GET':
        paginator = Paginator(data, numitems)
        page_obj = paginator.get_page(page)
        return render(request=request, template_name='list_reservations1.html', context={'reservations': page_obj})

    return redirect('list_reservations1')


@login_required
def list_reservations(request):
    data = get_reservations()
    return render(request=request, template_name='list_reservations.html', context={'reservations': data})


@login_required
def list_reservations1(request):
    data = get_reservations()
    return render(request=request, template_name='list_reservations1.html', context={'reservations': data})


@login_required
def list_reservations2(request):
    usernames = {}
    usernames.__setitem__('Todos', '')
    for usr in Group.objects.get(name='prop-dept').user_set.all().filter(is_staff=False).order_by('username'):
        usernames.__setitem__(usr.username, usr.username)

    common_area_names = {}
    common_area_names.__setitem__('Todos', '')
    for can in AreaComun.objects.all():
        common_area_names.__setitem__(can.nombre, can.nombre)

    status = {'Todos': '', 'Confirmado': 'Confirmado', 'Cancelado': 'Cancelado', 'Pendiente': 'Pendiente'}
    context = {
         'usernames': usernames,
         'common_area_names': common_area_names,
         'status': status
    }

    return render(request=request, template_name='list_reservations2.html', context=context)


def get_filters(request):
    filters = CustomFilters()
    filters.filter_username = request.GET.get('filter_username', '')
    filters.filter_common_area_name = request.GET.get('filter_common_area_name', '')
    date_param = request.GET.get('filter_begin_reservation_date', '')
    if date_param != '':
        date_object = datetime.strptime(date_param, '%m/%d/%Y')
        # date_param = date_object.strftime('%Y-%m-%d')
        date_param = date_object.date()
    filters.filter_begin_reservation_date = date_param
    filters.filter_status = request.GET.get('filter_status')

    return filters


def get_reservations_content(request):
    filters = get_filters(request)
    content = get_content(request, 'reservations_content.html', filters)
    return HttpResponse(content=content, content_type='text/html')


def get_content(request, template_name, filters):
    num_items = request.GET.get('num_items', 10)
    page = request.GET.get('page', 1)
    data = get_reservations()
    data.sort(key=lambda x: x.begin_reservation_date, reverse=True)
    filtered = get_filtered_data(data, filters)
    paginator = Paginator(filtered, num_items)
    page_obj = paginator.get_page(page)
    content = render_to_string(template_name, {'reservations': page_obj})

    return content


def get_filtered_data(data, filters):
    filtered = []
    index = 1
    for rsv in data:
        meets_condition = True
        meets_condition = check_filter(
            filter_key=filters.filter_username,
            data_value=rsv.username,
            meets_condition=meets_condition)
        meets_condition = check_filter(
            filter_key=filters.filter_common_area_name,
            data_value=rsv.common_area_name,
            meets_condition=meets_condition)
        meets_condition = check_filter(
            filter_key=filters.filter_status,
            data_value=rsv.status,
            meets_condition=meets_condition
        )
        meets_condition = check_filter(
            filter_key=filters.filter_begin_reservation_date,
            data_value=rsv.begin_reservation_date,
            meets_condition=meets_condition
        )

        print(filters.filter_begin_reservation_date)
        print(rsv.begin_reservation_date)

        if meets_condition:
            add_filtered(filtered, index, rsv)
            index = index + 1

    return filtered


def check_filter(filter_key, data_value, meets_condition):
    if filter_key == '':
        meets_condition = meets_condition and True
    else:
        if filter_key == data_value:
            meets_condition = meets_condition and True
        else:
            meets_condition = meets_condition and False

    return meets_condition


def add_filtered(filtered, index, rsv):
    rsv.row_number = index
    filtered.append(rsv)


def sort_by_begin_date(val):
    return val.begin_reservation_date


def get_pagination_content(request):
    filters = get_filters(request)
    content = get_content(request, 'pagination_content.html', filters)
    return HttpResponse(content=content, content_type='text/html')


def get_reservations():
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

            if receipt.is_canceled:
                reservation.status = 'Cancelado'
            elif receipt.is_reservation_confirmed:
                reservation.status = 'Confirmado'
            else:
                reservation.status = 'Pendiente'

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

            if rsv.confirmada:
                reservation.status = 'Confirmado'
            else:
                reservation.status = 'Pendiente'

        data.append(reservation)

    return data


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
    receipt_filename = f'receipt_{uuid.uuid4()}.pdf'
    receipts_path = os.path.join(settings.STATICFILES_DIRS[0], 'receipts/')

    if not os.path.exists(receipts_path):
        os.makedirs(receipts_path)

    receipt_filepath = os.path.join(receipts_path, receipt_filename)
    dest = open(receipt_filepath, 'w+b')
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
        blob_manager.upload_file(filename=receipt_filename, src_folder=receipts_path, content_type='application/pdf')

    return receipt_filename
