from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class UsuarioCreationForm(UserCreationForm):
    nome = forms.CharField(max_length=255, required=True, label="Nome Completo")
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Usuario
        fields = ('username', 'nome', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UsuarioLoginForm(AuthenticationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'password')
