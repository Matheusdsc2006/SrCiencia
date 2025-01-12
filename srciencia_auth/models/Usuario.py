from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

PERFIL = (
    (1, 'Admin'),
    (2, 'Aluno'),
    (3, 'Professor'),
)

class Usuario(AbstractUser):
    nome = models.CharField(max_length=255, blank=False, null=False, verbose_name="Nome Completo")
    perfil = models.IntegerField(choices=PERFIL, default=2)
    email = models.EmailField(unique=True)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True) 
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_alteracao = models.DateTimeField(auto_now=True)
    situacao = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.nome} - ({self.get_perfil_display()})'

@receiver(post_save, sender=AbstractUser)
def create_user_usuario(sender, instance, created, **kwargs):
    if created:
        Usuario.objects.create(username=instance.username, email=instance.email)

@receiver(post_save, sender=AbstractUser)
def save_user_usuario(sender, instance, **kwargs):
    try:
        instance.usuario.save()
    except Usuario.DoesNotExist:
        pass
