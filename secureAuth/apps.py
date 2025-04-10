from django.apps import AppConfig


class SecureauthConfig(AppConfig):
    name = 'secureAuth'
    verbose_name = 'Authentification et Sécurité'

    def ready(self):
        import secureAuth.signals
