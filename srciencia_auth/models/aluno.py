from srciencia_auth.models import *

class Aluno(models.Model):
    nome = models.CharField(max_length=255)
    matricula = models.IntegerField(unique=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    foto = models.ImageField(blank=True, null=True)
    perfil = models.CharField(max_length=100)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_acesso = models.DateTimeField(auto_now=True)
    situacao = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nome} - ({self.matricula})'