from django.shortcuts import render, redirect
from django.contrib.auth import login
from srciencia_auth.forms import UsuarioCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

def register(request, professor=False):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name, user.last_name = split_full_name(form.cleaned_data['nome'])
            user.perfil = 3 if professor else 2 
            user.is_staff = professor
            user.situacao = 'Regular'
            user.save()
            login(request, user)  
            return redirect('pagina_inicial') 
    else:
        form = UsuarioCreationForm()
    return render(request, './auth/cadastro.html', {'form': form, 'professor': professor})


def register_professor(request):
    return register(request, professor=True)


def split_full_name(full_name):
    """Divide o nome completo em primeiro e último nome."""
    parts = full_name.split()
    first_name = parts[0]
    last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
    return first_name, last_name
