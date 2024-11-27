import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'srciencia_admin.settings')  # Ajuste o caminho se necessário
django.setup()

from django.core.mail import send_mail

send_mail(
    'Teste de E-mail',
    'Este é um e-mail de teste enviado pelo Django utilizando a Brevo.',
    'seu_email@dominio.com',  # Substitua pelo remetente autenticado
    ['destinatario@dominio.com'],  # Substitua pelo destinatário
    fail_silently=False,
)
