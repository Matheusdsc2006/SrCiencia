from django.urls import path
from srciencia_core.views.adminView import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Gestão de Questões
    path('questoes/', questao_list, name='questao_list'),
    path("questoes/create", questao_create, name="questao_create"),
    path("questoes/edit/<int:pk>/", questao_update, name="questao_update"),
    path("questoes/delete/<int:pk>/", questao_delete, name="questao_delete"),

    # API de Conteúdos e Tópicos
    path('api/conteudos/<int:disciplina_id>/', get_conteudos, name='get_conteudos'),
    path('api/topicos/<int:conteudo_id>/', get_topicos, name='get_topicos'),

    # Adicionar Tipos
    path("gerenciar-banca/", gerenciar_banca, name="gerenciar_banca"),
    path("gerenciar_disciplina/", gerenciar_disciplina, name="gerenciar_disciplina"),
    path('gerenciar_banca/', gerenciar_banca, name='gerenciar_banca'),
    path('gerenciar_conteudo/', gerenciar_conteudo, name='gerenciar_conteudo'),
    path('gerenciar_topico/', gerenciar_topico, name='gerenciar_topico'),

    # Buscar tipos
    path("buscar_bancas/", buscar_bancas, name="buscar_bancas"),
    path('buscar_disciplinas/', buscar_disciplinas, name='buscar_disciplinas'),
    path("buscar_conteudos/", buscar_conteudos, name="buscar_conteudos"),
    path("buscar_topicos/", buscar_topicos, name="buscar_topicos"),

    # Remoção de Tipos
    path('remover/<str:tipo>/<int:id>/', remover_tipo, name='remover_tipo'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
