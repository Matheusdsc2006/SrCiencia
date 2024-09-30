from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UsuarioCreationForm, UsuarioLoginForm

def register(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # redirecionar para a página inicial ou outra página
    else:
        form = UsuarioCreationForm()
    return render(request, 'register.html', {'form': form})

