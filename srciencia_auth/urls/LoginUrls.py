from django.urls import path
from srciencia_auth.views.LoginView import login_view
from srciencia_auth.views.CadastroView import register
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/", login_view, name='login'),
    path("cadastro/", register, name='cadastro'),
    path('password_reset_form', auth_views.PasswordResetView.as_view(template_name='auth/password_reset_form.html'), name='password_reset_form'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
]