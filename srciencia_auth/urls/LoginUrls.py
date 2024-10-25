from django.urls import path
from srciencia_auth.views.LoginView import *
from srciencia_auth.views.CadastroView import register
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/", login_view, name='login'),
    path("cadastro/", register, name='cadastro'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', password_reset_done, name="password_reset_done"),
]