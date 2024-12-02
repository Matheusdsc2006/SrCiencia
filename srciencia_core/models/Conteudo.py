from django.db import models
from .Questao import Questao
from .Disciplina import Disciplina

class Conteudo(models.Model):
    nome = models.CharField(max_length=255)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name="conteudos")

    def __str__(self):
        return self.nome
    
class ConteudoQuestao(models.Model):
    conteudo = models.ForeignKey(Conteudo, on_delete=models.CASCADE)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)