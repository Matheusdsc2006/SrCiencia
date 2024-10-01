from django.shortcuts import render, redirect
from django.contrib.auth import login
from srciencia_auth.forms import UsuarioCreationForm
from srciencia_auth.models import Usuario 

def register(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  
            user.perfil = 2 
            user.situacao = 'Regular'  
            user.save()  
            login(request, user)
            return redirect('home')  
    else:
        form = UsuarioCreationForm()
    return render(request, './auth/cadastro.html', {'form': form})