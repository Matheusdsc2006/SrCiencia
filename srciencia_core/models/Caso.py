from django.db import models
from .Questao import Questao
from django_ckeditor_5.fields import CKEditor5Field

class Caso(models.Model):
    questao = models.ForeignKey(Questao, related_name='casos', on_delete=models.CASCADE)
    variaveis = models.JSONField(default=dict)
    resolucao = CKEditor5Field('resolucao', config_name='default')

    def __str__(self):
        return f"Caso da Questão {self.questao.id}"