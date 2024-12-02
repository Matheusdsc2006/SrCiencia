from django.db import models
from .Questao import Questao

class Disciplina(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome
    
class DisciplinaQuestao(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)