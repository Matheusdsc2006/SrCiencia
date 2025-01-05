from django import forms
from srciencia_core.models import Questao, Alternativa, Banca, Disciplina, Conteudo, Topico

class QuestaoForm(forms.ModelForm):
    class Meta:
        model = Questao
        fields = [
            "descricao", "banca", "disciplina", "conteudo", "topico", "resolucao", "alteravel"
        ]
        widgets = {
            'banca': forms.Select(),
            'disciplina': forms.Select(attrs={'id': 'id_disciplina'}),
            'conteudo': forms.Select(attrs={'id': 'id_conteudo', 'disabled': 'disabled'}),
            'topico': forms.Select(attrs={'id': 'id_topico', 'disabled': 'disabled'}),
            'alteravel': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['banca'].queryset = Banca.objects.all()
        self.fields['disciplina'].queryset = Disciplina.objects.all()

        # Adicionar uma opção inicial vazia
        self.fields['banca'].empty_label = "Selecione a banca examinadora"
        self.fields['disciplina'].empty_label = "Selecione a disciplina"
        self.fields['conteudo'].empty_label = "Selecione o conteúdo"
        self.fields['topico'].empty_label = "Selecione o tópico"

        # Habilitar "conteudo" e "topico" se valores já estiverem preenchidos (edição)
        if self.instance and self.instance.conteudo:
            self.fields['conteudo'].widget.attrs.pop('disabled', None)
        if self.instance and self.instance.topico:
            self.fields['topico'].widget.attrs.pop('disabled', None)

    def clean(self):
        cleaned_data = super().clean()
        disciplina = cleaned_data.get('disciplina')
        conteudo = cleaned_data.get('conteudo')
        topico = cleaned_data.get('topico')

        if conteudo and conteudo.disciplina != disciplina:
            raise forms.ValidationError("O conteúdo selecionado não pertence à disciplina escolhida.")

        if topico and topico.conteudo != conteudo:
            raise forms.ValidationError("O tópico selecionado não pertence ao conteúdo escolhido.")

        return cleaned_data


class AlternativaForm(forms.ModelForm):
    class Meta:
        model = Alternativa
        fields = ["descricao", "correta", "imagem"]
        widgets = {
            'descricao': forms.TextInput(attrs={'placeholder': 'Descrição da alternativa'}),
            'correta': forms.CheckboxInput(),
            'imagem': forms.ClearableFileInput(attrs={'style': 'display: none;'}),
        }


class BancaForm(forms.ModelForm):
    class Meta:
        model = Banca
        fields = ["nome"]
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Nome da Banca", "class": "form-control"}),
        }


class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ["nome"]
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Nome da Disciplina", "class": "form-control"}),
        }


class ConteudoForm(forms.ModelForm):
    class Meta:
        model = Conteudo
        fields = ["nome", "disciplina"]
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Nome do Conteúdo", "class": "form-control"}),
            "disciplina": forms.Select(attrs={"class": "form-select"}),
        }


class TopicoForm(forms.ModelForm):
    class Meta:
        model = Topico
        fields = ["nome", "conteudo"]
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Nome do Tópico", "class": "form-control"}),
            "conteudo": forms.Select(attrs={"class": "form-select"}),
        }

