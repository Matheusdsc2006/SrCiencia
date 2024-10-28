from django.urls import path
from srciencia_core.views.adminView import *

urlpatterns = [
    path("questoes/", questao_list, name="questao_list"),
    path("questoes/create", questao_create, name="questao_create"),
    path("questoes/edit/<int:pk>/", questao_update, name="questao_update"),
    path("questoes/delete/<int:pk>/", questao_delete, name="questao_delete"),
    
]
