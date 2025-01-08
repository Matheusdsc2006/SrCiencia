from django.db import models
from django.conf import settings

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
