from django.apps import AppConfig


class RedSocialConfig(AppConfig):
    name = 'red_social'

    # Definimos la funcion red social y le pasamos como parametro self
    # Importamos 'signals' desde la misma app
    def ready(self):
        import red_social.signals
