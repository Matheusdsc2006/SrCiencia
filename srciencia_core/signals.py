from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Questao
import re

def extrair_variaveis(texto):
    variaveis = re.findall(r'\{(.*?)\}', texto)
    return {var: None for var in variaveis}

@receiver(pre_save, sender=Questao)
def processar_variaveis(sender, instance, **kwargs):
    if instance.descricao:
        variaveis_extraidas = extrair_variaveis(instance.descricao)
        for caso in instance.casos.all():
            caso.variaveis.update(variaveis_extraidas)
            caso.save()
