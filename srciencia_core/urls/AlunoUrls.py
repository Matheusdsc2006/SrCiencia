from django.urls import path
from srciencia_core.views.praticarView import *
from srciencia_core.views.PerfilView import *

urlpatterns = [
    # Página inicial de prática para o aluno
    path('', aluno_praticar, name='aluno_praticar'),

    # Rota para buscar questões filtradas
    path('api/questoes', buscar_questoes, name='buscar_questoes'),

    # Rota para registrar a resposta do aluno
    path('registrar_resposta/', registrar_resposta, name='registrar_resposta'),

    # Rota para reportar um problema na questão
    path('reportar_questao/', reportar_questao, name='reportar_questao'),

    # Rota para finalizar a atividade
    path('finalizar_atividade/', finalizar_atividade, name='finalizar_atividade'),

    # Rota para exportar a atividade
    path("exportar/", exportar_atividade, name="exportar_atividade"),

    # Rota para favoritar questão
    path("favoritar_questao/<int:questao_id>/", favoritar_questao, name="favoritar_questao"),
]
