from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import smtplib
import ssl
from django.core.mail.backends.smtp import EmailBackend

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            if '@' in username:
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None


class CustomSMTPConnection(smtplib.SMTP):
    def starttls(self, keyfile=None, certfile=None):
        # Inicia TLS
        super().starttls(keyfile, certfile)

class CustomEmailBackend(EmailBackend):
    def open(self, fail_silently=False):
        # Criação da conexão com o servidor SMTP
        try:
            self.connection = CustomSMTPConnection(
                self.host,
                self.port,
                timeout=self.timeout,
            )
            if self.use_tls:
                # Removendo o parâmetro context
                self.connection.starttls()
            if self.username:
                self.connection.login(self.username, self.password)
            return True
        except Exception as e:
            if fail_silently:
                return False
            else:
                raise e

    def send_messages(self, email_messages):
        # Envio de mensagens de e-mail
        if not self.connection:
            self.open()
        return super().send_messages(email_messages)

    def close(self):
        # Fechamento da conexão
        if self.connection:
            self.connection.quit()
        super().close()
