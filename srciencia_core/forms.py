from django import forms
from .models import Questao, Banca, Disciplina, DisciplinaQuestao, Conteudo, Topico, Caso, Alternativa
from django_ckeditor_5.widgets import CKEditor5Widget

class QuestaoForm(forms.ModelForm):
    class Meta:
        model = Questao
        fields = ['descricao', 'banca', 'dificuldade']
        widgets = {
              "descricao": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="default"
              )
          }

class DisciplinaQuestaoForm(forms.Form):
    disciplina = forms.ModelChoiceField(queryset=Disciplina.objects.all())
    conteudo = forms.ModelChoiceField(queryset=Conteudo.objects.all())
    topico = forms.ModelChoiceField(queryset=Topico.objects.all())

class CasoForm(forms.ModelForm):
    class Meta:
        model = Caso
        fields = ['variaveis', 'resolucao']
        widgets = {
              "resolucao": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="default"
              )
          }

class AlternativaForm(forms.ModelForm):
    class Meta:
        model = Alternativa
        fields = ['descricao', 'imagem', 'correta']

CasoFormSet = forms.modelformset_factory(Caso, form=CasoForm, extra=1)
AlternativaFormSet = forms.inlineformset_factory(Caso, Alternativa, form=AlternativaForm, extra=1)
DisciplinaQuestaoFormSet = forms.modelformset_factory(DisciplinaQuestao, fields=('disciplina',), extra=1)

