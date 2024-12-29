from django.contrib import admin
from .models import *
from srciencia_core.models.Turma import Turma


class UsuarioAdmin(admin.ModelAdmin):
    date_hierarchy = 'data_cadastro'
    list_display = ('nome', 'email', 'perfil', 'situacao',)
    empty_value_display = 'Vazio'

admin.site.register(Usuario, UsuarioAdmin)

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'professor', 'codigo', 'criado_em')  
    search_fields = ('nome', 'professor__username', 'codigo') 
    list_filter = ('criado_em',) 
    ordering = ('-criado_em',)  