from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    codigo = models.CharField(max_length=8, unique=True)
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="turmas_criadas")
    alunos = models.ManyToManyField(User, related_name="turmas_inscritas", blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
