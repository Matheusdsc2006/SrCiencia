from django.apps import AppConfig


class SrcienciaCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'srciencia_core'

    def ready(self):
        import srciencia_core.signals 