
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from srciencia_core.views.adminView import get_topicos, get_conteudos
from srciencia_core.views.Visualizar_alunosView import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('srciencia_auth.urls.HomeUrls')),
    path('auth/', include('srciencia_auth.urls.LoginUrls')),
    path('app/u/0/', include('srciencia_core.urls.adminUrls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/conteudos/<int:disciplina_id>/', get_conteudos, name='get_conteudos'),
    path('api/topicos/<int:conteudo_id>/', get_topicos, name='get_topicos'),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('pagina_inicial/', include('srciencia_core.urls.Pagina_inicialUrls')),
    path('turmas/', include('srciencia_core.urls.TurmasUrls')),
    path('professor_turmas/', include('srciencia_core.urls.Professor_turmasUrls')),
    path('turmas/<int:turma_id>/alunos/', listar_alunos_turma, name='listar_alunos_turma'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
