from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from srciencia_auth.forms import UsuarioLoginForm, PasswordResetForm, AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views import View
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.http import JsonResponse

def login_api_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return JsonResponse({"is_admin": user.is_superuser})
    return JsonResponse({"error": "Invalid login"}, status=400)


def login_view(request):
    if request.method == 'POST':
        form = UsuarioLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                request.session['conta_atual'] = user.email
                request.session.modified = True
                
                if user.is_superuser:
                    return redirect('questao_list') 
                return redirect('pagina_inicial')  
            else:
                messages.error(request, "Credenciais inválidas. Por favor, tente novamente.")
    else:
        form = UsuarioLoginForm() 
    return render(request, './auth/login.html', {'form': form})


def password_reset_done(request):
    return render(request, './auth/password_reset_done.html')


class CustomPasswordResetView(View):
    def get(self, request):
        form = PasswordResetForm()
        return render(request, 'auth/password_reset_form.html', {'form': form})

    def post(self, request):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "E-mail não encontrado.")
                return render(request, 'auth/password_reset_form.html', {'form': form})

            # Geração do token e envio do e-mail
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            link = f"http://127.0.0.1:8000/auth/password_reset_confirm/{uid}/{token}/"
            subject = "Redefinição de Senha"
            message = render_to_string('auth/password_reset_email.html', {'link': link})
            send_mail(subject, message, 'from@example.com', [email])  # Ajuste o sender
            messages.success(request, "Instruções de redefinição de senha enviadas para seu e-mail.")
            return redirect('password_reset_done')
        return render(request, 'auth/password_reset_form.html', {'form': form})


class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        # Decodifique o uid e verifique o token aqui
        # Se válido, exiba um formulário para redefinir a senha
        form = SetPasswordForm(user)
        return render(request, 'auth/password_reset_confirm.html', {'form': form})

    def post(self, request, uidb64, token):
        # Verifique o token novamente e redefina a senha
        user = get_user_model()._default_manager.get(pk=urlsafe_base64_decode(uidb64).decode())
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sua senha foi redefinida com sucesso.")
            return redirect('login')
        return render(request, 'auth/password_reset_confirm.html', {'form': form})
