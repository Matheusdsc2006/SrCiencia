from django.db import models
from .Caso import Caso

class Alternativa(models.Model):
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE, related_name="alternativas")
    descricao = models.CharField(max_length=255)
    imagem = models.ImageField(upload_to='alternativas/', blank=True, null=True)
    correta = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Alternativa {self.id} - {'Correta' if self.correta else 'Incorreta'}"