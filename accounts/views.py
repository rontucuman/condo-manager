from django.contrib.auth import logout, get_user_model
from django.contrib.auth.models import Group, User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from condomanager.email.SingleAzureEmailSender import SingleAzureEmailSender
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required

import json


# Create your views here.


def testemailview(request):
    return render(request, 'email/user_registered.html')


def send_email(user, operation):
    subject = ''
    template_name = ''

    if operation == 'register':
        subject = 'Cuenta en Condo Manager creada'
        template_name = 'email/user_registered.html'
    elif operation == 'activate':
        subject = 'Cuenta en Condo Manager activada'
        template_name = 'email/user_activated.html'
    elif operation == 'inactivate':
        subject = 'Cuenta en Condo Manager inactivada'
        template_name = 'email/user_inactivated.html'

    if subject != '':
        html_message = render_to_string(template_name, {'username': user.username})
        plain_message = strip_tags(html_message)
        mail_to = user.email
        email_sender = SingleAzureEmailSender()
        email_sender.send_message(
            subject=subject,
            content_plain=plain_message,
            content_html=html_message,
            mail_to=mail_to)


def register_user(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user_group = Group.objects.get(name='prop-dept')

            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()
            send_email(new_user, 'register')

            user_group.user_set.add(new_user)
            user_group.save()

            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register_user.html', {'form': user_form})

@login_required()
def logout_account(request):
    logout(request)
    return redirect('register_user')


# def login_account(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request,
#                                 username=cd['username'],
#                                 password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#         form = LoginForm()
#     return render(request, 'login_account.html', {'login_form': form})


@login_required()
def dashboard(request):
    return render(request, 'dashboard.html', {'section': 'dashboard'})


@login_required()
def activate_acct(request):
    users = Group.objects.get(name='prop-dept').user_set.all().filter(is_staff=False).order_by('username')
    user_list = list()
    user_counter = 1
    new_object = lambda **kwargs: type("Object", (), kwargs)
    for usr in users:
        user_list.append(
            new_object(
                counter=user_counter,
                id=usr.id,
                username=usr.username,
                email=usr.email,
                is_active=usr.is_active))
        user_counter = user_counter + 1

    return render(request, 'activate_acct.html', {'users': user_list})


@login_required()
def process_active_change(request):
    if request.method == 'POST':
        try:
            user_id = request.POST['user_id']
            is_checked = json.loads(request.POST['is_checked'].lower())
            user = User.objects.filter(id=user_id).first()
            user.is_active = is_checked
            user.save()

            if is_checked:
                send_email(user, 'activate')
            else:
                send_email(user, 'inactivate')

            return HttpResponse(f"El usuario {user.username} esta ahora {'activado' if is_checked else 'inactivado'}")
        except:
            return HttpResponse("No se pudo guardar el cambio de estado. Intentelo nuevamente.")

    else:
        return HttpResponse("No se pudo guardar el cambio de estado. Intentelo nuevamente.")
