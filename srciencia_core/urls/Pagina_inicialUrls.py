from django.urls import path
from srciencia_core.views.Visualizar_inicioView import *

urlpatterns = [
    path('', pagina_inicial, name='pagina_inicial'),
]
