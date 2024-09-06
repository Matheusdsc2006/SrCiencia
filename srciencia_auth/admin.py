from django.contrib import admin
from .models import *
# Register your models here.
class UsuarioAdmin(admin.ModelAdmin):
    date_hierarchy = 'data_cadastro'
    list_display = ('nome', 'matricula', 'email', 'perfil', 'situacao',)
    empty_value_display = 'Vazio'

admin.site.register(Usuario, UsuarioAdmin)