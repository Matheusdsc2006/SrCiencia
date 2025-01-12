from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from srciencia_core.views.adminView import get_topicos, get_conteudos
from srciencia_core.views.Visualizar_alunosView import listar_alunos_turma

urlpatterns = [
    # Administração
    path('admin/', admin.site.urls),

    # Autenticação
    path('', include('srciencia_auth.urls.HomeUrls')),
    path('auth/', include('srciencia_auth.urls.LoginUrls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # APIs
    path('api/conteudos/<int:disciplina_id>/', get_conteudos, name='get_conteudos'),
    path('api/topicos/<int:conteudo_id>/', get_topicos, name='get_topicos'),

    # CKEditor
    path("ckeditor5/", include('django_ckeditor_5.urls')),

    # Funcionalidades gerais
    path('pagina_inicial/', include('srciencia_core.urls.Pagina_inicialUrls')),
    path('turmas/', include('srciencia_core.urls.TurmasUrls')),

    # Perfis
    path('perfil/', include('srciencia_core.urls.PerfilUrls')),  # Roteamento para os perfis

    # Funcionalidades do professor e aluno
    path('professor_turmas/', include('srciencia_core.urls.ProfessorUrls')),
    path('aluno/', include('srciencia_core.urls.AlunoUrls')),

    # Turmas específicas
    path('turmas/<int:turma_id>/alunos/', listar_alunos_turma, name='listar_alunos_turma'),
]

# Arquivos estáticos e mídia
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
