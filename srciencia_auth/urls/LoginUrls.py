from django.urls import path
from srciencia_auth.views.LoginView import login_view
from srciencia_auth.views.CadastroView import register

urlpatterns = [
    path("login/", login_view, name='login'),
    path("cadastro/", register, name='login'),
]