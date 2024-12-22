from django.urls import path
from srciencia_core.views.Professor_turmasView import *
from srciencia_core.views.Visualizar_alunosView import *
from srciencia_core.views.Excluir_turmaView import *

urlpatterns = [
    path("", professor_turmas, name="professor_turmas"), 
    path("criar/", criar_turma, name="criar_turma"), 
    path('turmas/<int:turma_id>/alunos/', alunos_turma_view, name='alunos_turma'),
    path('excluir_turma/<int:id>/', excluir_turma, name='excluir_turma'),
]
