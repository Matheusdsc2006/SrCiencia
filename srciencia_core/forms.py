from django import forms
from srciencia_core.models import Questao, Alternativa, Banca, Disciplina, Conteudo, Topico

class QuestaoForm(forms.ModelForm):
    class Meta:
        model = Questao
        fields = [
            "descricao", "banca", "disciplina", "conteudo", "topico", "resolucao"
        ]
        widgets = {
            'banca': forms.Select(attrs={'placeholder': 'Selecione a banca examinadora'}),
            'disciplina': forms.Select(attrs={'placeholder': 'Selecione a disciplina', 'id': 'id_disciplina'}),
            'conteudo': forms.Select(attrs={'placeholder': 'Selecione o conteúdo', 'id': 'id_conteudo', 'disabled': 'disabled'}),
            'topico': forms.Select(attrs={'placeholder': 'Selecione o tópico', 'id': 'id_topico', 'disabled': 'disabled'}),
            'alteravel': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['banca'].queryset = Banca.objects.all()
        self.fields['disciplina'].queryset = Disciplina.objects.all()




class AlternativaForm(forms.ModelForm):
    class Meta:
        model = Alternativa
        fields = ["descricao", "correta", "imagem"] 
        widgets = {
            'descricao': forms.TextInput(attrs={'placeholder': 'Descrição da alternativa'}),
            'correta': forms.CheckboxInput(),
            'imagem': forms.ClearableFileInput(attrs={'style': 'display: none;'}),
        }