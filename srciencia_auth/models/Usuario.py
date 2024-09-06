from srciencia_auth.models import *

class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    matricula = models.IntegerField(unique=True)
    perfil = models.IntegerField(choices=PERFIL, default=2)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    foto = models.ImageField(blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_alteracao = models.DateTimeField(auto_now=True)
    situacao = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nome} - ({self.matricula})'
    
    @receiver(post_save, sender=User)
    def create_user_usuario(sender, instance, created, **kwargs):
        try:
            if created:
                Usuario.objects.create(user=instance)
        except: 
            pass
    
    @receiver(post_save, sender=User)
    def save_user_usuario(sender, instance, **kwargs):
        try:
            instance.usuario.save()
        except:
            pass