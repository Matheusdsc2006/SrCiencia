from django import forms
from srciencia_core.models import Questao, Alternativa

class QuestaoForm(forms.ModelForm):
    class Meta:
        model = Questao
        fields = ["descricao", "banca", "dica", "pontuacao"]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descrição da questão'}),
            'banca': forms.TextInput(attrs={'placeholder': 'Banca examinadora (opcional)'}),
            'dica': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Dica (opcional)'}),
            'pontuacao': forms.NumberInput(attrs={'placeholder': 'Pontuação'}),
        }

class AlternativaForm(forms.ModelForm):
    class Meta:
        model = Alternativa
        fields = ["descricao", "correta"]
        widgets = {
            'descricao': forms.TextInput(attrs={'placeholder': 'Descrição da alternativa'}),
            'correta': forms.CheckboxInput(),
        }
