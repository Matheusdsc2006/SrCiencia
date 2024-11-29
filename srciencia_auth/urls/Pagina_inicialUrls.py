from django.urls import path
from srciencia_auth.views.Visualizar_inicioView import pagina_inicial

urlpatterns = [
    path('pagina_inicial/', pagina_inicial, name='pagina_inicial'),
]
