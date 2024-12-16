from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario
from django.contrib.auth import get_user_model

class UsuarioCreationForm(UserCreationForm):
    nome = forms.CharField(max_length=255, required=True, label="Nome Completo")
    email = forms.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ('username', 'nome', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Digite seu nome de usuário',
            'nome': 'Digite seu nome completo',
            'email': 'Digite seu e-mail',
            'password1': 'Digite sua senha',
            'password2': 'Confirme sua senha'
        }
        for field in self.fields:
            if field in placeholders:
                self.fields[field].widget.attrs['placeholder'] = placeholders[field]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.nome = self.cleaned_data['nome']  # Salvar o nome completo
        if commit:
            user.save()
        return user

class UsuarioLoginForm(AuthenticationForm):
    username = forms.CharField(label="Nome de Usuário ou E-mail")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Digite seu nome de usuário ou e-mail'
        self.fields['password'].widget.attrs['placeholder'] = 'Digite sua senha'

    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        User = get_user_model()

        if User.objects.filter(email=username_or_email).exists():
            self.cleaned_data['username'] = User.objects.get(email=username_or_email).username

        return super().clean()

class PasswordResetForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Digite seu e-mail'
