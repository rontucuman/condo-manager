from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('signupaccount/', views.register_user, name='register_user'),
    # path('logout/', views.logout_account, name='logout_account'),
    # path('login/', views.login_account, name='login_account'),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login_account.html'), name='login_account'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='registration/logout_account.html'), name='logout_account'),
    path('', views.dashboard, name='dashboard'),
]
