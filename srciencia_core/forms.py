from django import forms
from django.forms import BaseModelFormSet, ValidationError
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
        fields = ["descricao", "correta", "imagem_url"]
        widgets = {
            'descricao': forms.TextInput(attrs={'placeholder': 'Descrição da alternativa'}),
            'correta': forms.CheckboxInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        descricao = cleaned_data.get("descricao")
        imagem_url = cleaned_data.get("imagem_url")

        # Verificar apenas os formulários realmente enviados
        if not descricao and not imagem_url:
            raise forms.ValidationError("A descrição ou a URL da imagem deve ser preenchida.")

        return cleaned_data


class CustomAlternativaFormSet(BaseModelFormSet):
    def clean(self):
        """Valida se há pelo menos 1 alternativa correta."""
        super().clean()
        alternativas_validas = [
            form for form in self.forms if form.cleaned_data and not form.cleaned_data.get('DELETE', False)
        ]
        if not any(form.cleaned_data.get('correta', False) for form in alternativas_validas):
            raise ValidationError("Pelo menos uma alternativa deve ser marcada como correta.")


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
    disciplina = forms.ModelChoiceField(
        queryset=Disciplina.objects.all(),
        empty_label="---------",
        widget=forms.Select(attrs={"class": "form-select", "id": "id_disciplina"})
    )

    class Meta:
        model = Topico
        fields = ["nome", "disciplina", "conteudo"]
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Ex.: Densidade", "class": "form-control"}),
            "conteudo": forms.Select(attrs={"class": "form-select", "id": "id_conteudo", "disabled": "disabled"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["conteudo"].queryset = Conteudo.objects.none()

        if "disciplina" in self.data:
            try:
                disciplina_id = int(self.data.get("disciplina"))
                self.fields["conteudo"].queryset = Conteudo.objects.filter(disciplina_id=disciplina_id)
                self.fields["conteudo"].widget.attrs.pop("disabled", None)
            except (ValueError, TypeError):
                pass 
        elif self.instance.pk and self.instance.conteudo:
            self.fields["conteudo"].queryset = self.instance.conteudo.disciplina.conteudos.all()
            self.fields["conteudo"].widget.attrs.pop("disabled", None)

