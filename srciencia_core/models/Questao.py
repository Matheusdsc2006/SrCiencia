from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

DIFICULDADE = {
    (1, 'Fácil'),
    (2, 'Médio'),
    (3, 'Difícil'),
}

class Banca(models.Model):
    nome = models.CharField(max_length=255)
    def __str__(self):
        return self.nome

class Disciplina(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Conteudo(models.Model):
    nome = models.CharField(max_length=255)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name="conteudos")

    def __str__(self):
        return self.nome

class Topico(models.Model):
    nome = models.CharField(max_length=255)
    conteudo = models.ForeignKey(Conteudo, on_delete=models.CASCADE, related_name="topicos")

    def __str__(self):
        return self.nome

class Questao(models.Model):
    descricao = CKEditor5Field('descricao', config_name='default')
    alteravel = models.BooleanField(default=False)
    banca = models.ForeignKey(Banca, on_delete=models.SET_NULL, null=True, blank=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.SET_NULL, null=True, blank=True)
    conteudo = models.ForeignKey(Conteudo, on_delete=models.SET_NULL, null=True, blank=True)
    topico = models.ForeignKey(Topico, on_delete=models.SET_NULL, null=True, blank=True)
    resolucao = CKEditor5Field('resolucao', config_name='default', blank=True, null=True)
    dificuldade = models.IntegerField(choices=DIFICULDADE, default=1)
    ano = models.PositiveIntegerField(null=True, blank=True, verbose_name="Ano") 
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    taxa_acertos = models.FloatField(default=0, verbose_name="Taxa de Acertos (%)")  # Novo campo

    def __str__(self):
        return f"Questão {self.id}: {self.descricao[:50]}"

    def calcular_dificuldade(self):
        """
        Atualiza a dificuldade da questão com base na taxa de acertos.
        """
        if self.taxa_acertos >= 67:
            self.dificuldade = 1  # Fácil
        elif 34 <= self.taxa_acertos < 67:
            self.dificuldade = 2  # Médio
        else:
            self.dificuldade = 3  # Difícil
        self.save()




class Alternativa(models.Model):
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name="alternativas")
    descricao = models.CharField(max_length=255, blank=True)
    imagem = models.ImageField(upload_to='alternativas/', blank=True, null=True)
    correta = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    imagem_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"Alternativa {self.id} - {'Correta' if self.correta else 'Incorreta'}"