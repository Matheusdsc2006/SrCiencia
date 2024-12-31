from django.urls import path
from srciencia_auth.views.HomeView import home_view


urlpatterns = [
    path("", home_view, name='home'),
]