from django.urls import path
from srciencia_core.views.adminView import crud_questoes

urlpatterns = [
    path("questoes", crud_questoes, name='crud_questoes'),
]