from django.urls import path
from srciencia_core.views.TurmasView import *
from srciencia_core.views.Verificar_codigoView import *

urlpatterns = [
    path("", turmas_view, name="turmas"),
    path("mudar-conta/", mudar_conta, name="mudar_conta"),
    path("remover-conta/", remover_conta, name="remover_conta"),
    path('listar-contas/', listar_contas, name='listar_contas'),
    path("listar_turmas/", listar_turmas, name="listar_turmas"),
    path('confirmar-mudanca-conta/', confirmar_mudanca_conta, name='confirmar_mudanca_conta'),
    path("verificar_codigo_turma/", verificar_codigo_turma, name="verificar_codigo_turma"),
    path("<int:turma_id>/cancelar/", cancelar_inscricao, name="cancelar_inscricao"),
    path('listar_anexos_pendentes/', listar_anexos_pendentes, name='listar_anexos_pendentes'),
    path('marcar_anexos_vistos/', marcar_anexos_vistos, name='marcar_anexos_vistos'),
]
