from django.urls import path
from srciencia_core.views.PerfilView import aluno_perfil, professor_perfil, editar_apelido, editar_foto

urlpatterns = [
    path('aluno/', aluno_perfil, name='aluno_perfil'),  
    path('professor/', professor_perfil, name='professor_perfil'), 
    path('editar_apelido/', editar_apelido, name='editar_apelido'),
    path('editar_foto/', editar_foto, name='editar_foto'),
]
