from django.urls import path
from srciencia_auth.views.TurmasView import turmas_view, pendentes_view, cancelar_inscricao

urlpatterns = [
    path('turmas/', turmas_view, name='turmas'), 
    path('<int:turma_id>/pendentes/', pendentes_view, name='pendentes'),
    path('<int:turma_id>/cancelar/', cancelar_inscricao, name='cancelar_inscricao'),
]
