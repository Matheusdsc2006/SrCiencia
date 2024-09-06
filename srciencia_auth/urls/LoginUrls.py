from django.urls import path
from srciencia_auth.views.LoginView import login_view

urlpatterns = [
    path("login/", login_view, name='login'),
]