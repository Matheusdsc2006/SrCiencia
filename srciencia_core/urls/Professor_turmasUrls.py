from django.urls import path
from srciencia_core.views.Professor_turmasView import *
from srciencia_core.views.Visualizar_alunosView import *
from srciencia_core.views.Excluir_turmaView import *
from srciencia_core.views.praticarView import *

urlpatterns = [
    path("", professor_turmas, name="professor_turmas"), 
    path("criar/", criar_turma, name="criar_turma"),
    path('professor_turmas/listar_turmas/', listar_turmas_professor, name='listar_turmas_professor'),
    path('turmas/<int:turma_id>/alunos/', listar_alunos_turma, name='listar_alunos_turma'),
    path("upload_arquivo/<int:turma_id>/", upload_arquivo, name="upload_arquivo"),
    path("listar_arquivos/<int:turma_id>/", listar_arquivos, name="listar_arquivos"),
    path("remover_arquivo/<int:arquivo_id>/", remover_arquivo, name="remover_arquivo"),
    path('excluir_turma/<int:id>/', excluir_turma, name='excluir_turma'),
]
