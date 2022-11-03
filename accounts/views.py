from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from condomanager.email.SingleAzureEmailSender import SingleAzureEmailSender
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required


# Create your views here.


def testemailview(request):
    return render(request, 'email/user_registered.html')


def send_email(user):
    html_message = render_to_string('email/user_registered.html', {'username': user.username})
    plain_message = strip_tags(html_message)

    subject = 'Condo-Manager user created successfully'
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
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()

            send_email(new_user)

            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register_user.html', {'form': user_form})


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


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'section': 'dashboard'})
