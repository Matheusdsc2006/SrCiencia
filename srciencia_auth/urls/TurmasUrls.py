from django.urls import path
from srciencia_core.views.TurmasView import turmas_view, pendentes_view, cancelar_inscricao, mudar_conta, listar_contas, remover_conta

urlpatterns = [
    path("", turmas_view, name="turmas"),
    path("mudar-conta/", mudar_conta, name="mudar_conta"),
    path("remover-conta/", remover_conta, name="remover_conta"),
    path('listar-contas/', listar_contas, name='listar_contas'),
    path("pendentes/<int:turma_id>/", pendentes_view, name="pendentes"),
    path("cancelar-inscricao/<int:turma_id>/", cancelar_inscricao, name="cancelar_inscricao"),
]
