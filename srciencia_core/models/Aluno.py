from django.db import models
from srciencia_core.models import Turma

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='alunos')