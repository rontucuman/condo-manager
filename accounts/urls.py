from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('signup-account/', views.register_user, name='register_user'),
    # path('logout/', views.logout_account, name='logout_account'),
    # path('login/', views.login_account, name='login_account'),

    # login and logout urls
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login_account.html'), name='login_account'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='registration/logout_account.html'), name='logout_account'),

    # change password urls
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name="registration/password_change.html"), name="password_change"),
    path('password-change/done', auth_views.PasswordChangeDoneView.as_view(
        template_name="registration/password_change_done.html"), name="password_change_done"),

    # reset password urls
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset.html"), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html"), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html"), name="password_reset_confirm"),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html"), name="password_reset_complete"),

    path('', views.dashboard, name='dashboard'),
]
