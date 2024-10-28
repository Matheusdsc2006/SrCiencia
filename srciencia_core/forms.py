from django import forms
from srciencia_core.models import Questao, Alternativa, Banca, Disciplina, Conteudo, Topico

class QuestaoForm(forms.ModelForm):
    class Meta:
        model = Questao
        fields = [
            "descricao", "banca", "disciplina", "conteudo", "topico", "alteravel", "resolucao"
        ]
        widgets = {
            'banca': forms.Select(attrs={'placeholder': 'Selecione a banca examinadora'}),
            'disciplina': forms.Select(attrs={'placeholder': 'Selecione a disciplina', 'id': 'id_disciplina'}),
            'conteudo': forms.Select(attrs={'placeholder': 'Selecione o conteúdo', 'id': 'id_conteudo', 'disabled': 'disabled'}),
            'topico': forms.Select(attrs={'placeholder': 'Selecione o tópico', 'id': 'id_topico', 'disabled': 'disabled'}),
            'alteravel': forms.CheckboxInput(),
            'resolucao': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Resolução ou explicação detalhada da questão'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['banca'].queryset = Banca.objects.all()
        self.fields['disciplina'].queryset = Disciplina.objects.all()




class AlternativaForm(forms.ModelForm):
    class Meta:
        model = Alternativa
        fields = ["descricao", "correta", "imagem"]  # Adiciona imagem
        widgets = {
            'descricao': forms.TextInput(attrs={'placeholder': 'Descrição da alternativa'}),
            'correta': forms.CheckboxInput(),
        }

