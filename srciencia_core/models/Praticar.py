from django.db import models
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from srciencia_core.models.Questao import Questao, Banca, Disciplina, Conteudo, Topico
from django.db.models import Count, Case, When, F, FloatField

# Modelo RespostaAluno
class RespostaAluno(models.Model):
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='respostas')
    questao = models.ForeignKey('Questao', on_delete=models.CASCADE, related_name='respostas')
    alternativa_selecionada = models.ForeignKey('Alternativa', on_delete=models.SET_NULL, null=True, blank=True, related_name='respostas')
    correta = models.BooleanField(default=False)  # Indica se a resposta está correta
    data_resposta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Resposta de {self.aluno} - Questão: {self.questao.id}'

# Modelo RelatorioQuestao
class RelatorioQuestao(models.Model):
    questao = models.ForeignKey('Questao', on_delete=models.CASCADE, related_name='relatorios')
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='relatorios')
    descricao_problema = models.TextField()
    data_relatorio = models.DateTimeField(auto_now_add=True)
    resolvido = models.BooleanField(default=False)  # Indica se o problema foi resolvido pelo administrador

    def __str__(self):
        return f'Relatório: {self.questao.id} - {self.aluno}'

@login_required
def buscar_questoes(request):
    if request.method == 'GET':
        # Obtendo filtros
        disciplina_id = request.GET.get('disciplina')
        conteudo_id = request.GET.get('conteudo')
        dificuldade = request.GET.get('dificuldade')
        quantidade = int(request.GET.get('quantidade', 10))  # Padrão: 10 questões
        status_nao_resolvidas = 'nao_resolvidas' in request.GET.getlist('status', [])
        status_com_resolucao = 'com_resolucao' in request.GET.getlist('status', [])
        status_que_errei = 'que_errei' in request.GET.getlist('status', [])

        # Base inicial de questões
        questoes = Questao.objects.select_related('banca', 'disciplina', 'conteudo', 'topico').annotate(
            total_respostas=Count('respostas'),
            total_acertos=Count(Case(When(respostas__correta=True, then=1))),
            acuracia=Case(
                When(total_respostas=0, then=1.0),  # Se não há respostas, considera 100% de acerto
                default=F('total_acertos') / F('total_respostas'),
                output_field=FloatField()
            )
        )

        # Aplicando filtros
        if disciplina_id:
            questoes = questoes.filter(disciplina_id=disciplina_id)
        if conteudo_id:
            questoes = questoes.filter(conteudo_id=conteudo_id)
        if dificuldade:
            dificuldade_map = {
                '1': (0.67, 1.0),  # Fácil: 67%-100% de acerto
                '2': (0.34, 0.66),  # Médio: 34%-66% de acerto
                '3': (0.0, 0.33),   # Difícil: 0%-33% de acerto
            }
            if dificuldade in dificuldade_map:
                questoes = questoes.filter(acuracia__gte=dificuldade_map[dificuldade][0], acuracia__lte=dificuldade_map[dificuldade][1])

        # Filtros de status
        if status_nao_resolvidas:
            questoes = questoes.filter(respostas__isnull=True)
        if status_com_resolucao:
            questoes = questoes.exclude(resolucao__isnull=True).exclude(resolucao='')
        if status_que_errei:
            questoes = questoes.filter(respostas__aluno=request.user, respostas__correta=False)

        # Limitar quantidade de questões
        questoes = questoes[:quantidade]

        # Serializar resultados
        data = [
            {
                'id': questao.id,
                'descricao': questao.descricao,
                'alternativas': list(questao.alternativas.values('id', 'descricao', 'correta')),
                'resolucao': questao.resolucao,
                'ano': questao.ano,
                'banca': questao.banca.nome if questao.banca else None,
                'disciplina': questao.disciplina.nome if questao.disciplina else None,
                'conteudo': questao.conteudo.nome if questao.conteudo else None,
                'topico': questao.topico.nome if questao.topico else None,
            }
            for questao in questoes
        ]
        return JsonResponse({'questoes': data})

    return JsonResponse({'error': 'Método não permitido'}, status=405)


