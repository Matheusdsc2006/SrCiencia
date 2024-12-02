from django.db import models
from .Banca import Banca
from django_ckeditor_5.fields import CKEditor5Field


DIFICULDADE = {
    (1, 'Fácil'),
    (2, 'Médio'),
    (3, 'Difícil'),
}

class Questao(models.Model):
    descricao = CKEditor5Field('descricao', config_name='default')
    banca = models.ForeignKey(Banca, on_delete=models.SET_NULL, null=True, blank=True)
    dificuldade = models.IntegerField(choices=DIFICULDADE, default=1)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Questão {self.id}: {self.descricao[:50]}"


