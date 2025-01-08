from django.urls import path
from srciencia_core.views.praticarView import aluno_praticar, buscar_questoes, registrar_resposta, reportar_questao

urlpatterns = [
    # Página inicial de prática para o aluno
    path('', aluno_praticar, name='aluno_praticar'),

    # Rota para buscar questões filtradas
    path('buscar_questoes/', buscar_questoes, name='buscar_questoes'),

    # Rota para registrar a resposta do aluno
    path('registrar_resposta/', registrar_resposta, name='registrar_resposta'),

    # Rota para reportar um problema na questão
    path('reportar_questao/', reportar_questao, name='reportar_questao'),
]
