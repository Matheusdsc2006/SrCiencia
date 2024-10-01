from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from srciencia_auth.forms import UsuarioLoginForm

def login_view(request):
    if request.method == 'POST':
        form = UsuarioLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # redirecionar para a página inicial ou outra página
    else:
        form = UsuarioLoginForm()
    return render(request, './auth/login.html', {'form': form})
