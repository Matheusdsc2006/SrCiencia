from django.db import models

class Questao(models.Model):
    descricao = models.TextField()
    banca = models.CharField(max_length=255, blank=True, null=True)  
    dica = models.TextField(blank=True, null=True)  
    pontuacao = models.DecimalField(max_digits=5, decimal_places=2) 
    data_criacao = models.DateTimeField(auto_now_add=True) 
    data_atualizacao = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"Questão {self.id}: {self.descricao[:50]}"


class Alternativa(models.Model):
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name="alternativas")
    descricao = models.CharField(max_length=255)
    correta = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True) 
    data_atualizacao = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"Alternativa {self.id} - {'Correta' if self.correta else 'Incorreta'}"
