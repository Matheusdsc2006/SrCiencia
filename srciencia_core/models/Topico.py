from django.db import models
from .Questao import Questao
from .Conteudo import Conteudo

class Topico(models.Model):
    nome = models.CharField(max_length=255)
    conteudo = models.ForeignKey(Conteudo, on_delete=models.CASCADE, related_name="topicos")

    def __str__(self):
        return self.nome
    
class TopicoQuestao(models.Model):
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)