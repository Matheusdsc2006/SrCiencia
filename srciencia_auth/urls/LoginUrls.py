from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from srciencia_auth.views.LoginView import *
from srciencia_auth.views.CadastroView import *

urlpatterns = [
    path("login/", login_view, name="login"),
    path("cadastro/", register, name="cadastro"),
    path("cadastro_professor/", register_professor, name="cadastro_professor"),

    # URLs para redefinição de senha
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="auth/password_reset_form.html",
        email_template_name="auth/password_reset_email.html",
        success_url=reverse_lazy('password_reset_done')
    ), name="password_reset"),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(
        template_name="auth/password_reset_done.html"
    ), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="auth/password_reset_confirm.html"
    ), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="auth/password_reset_complete.html"
    ), name="password_reset_complete"),
]
