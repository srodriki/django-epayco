from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, DjangoRuntimeWarning


class DjangoEpaycoAppConfig(AppConfig):
    name = 'django_epayco'
    verbose_name = 'Django ePayco'

    def ready(self):
        if not settings.EPAYCO_PRIVATE_KEY:
            raise ImproperlyConfigured(self.name + ': EPAYCO_PRIVATE_KEY is not defined in your application\'s '
                                                   'settings. Please set your ePayco Account\'s Private Key before '
                                                   'using this package')

        if not settings.EPAYCO_PUBLIC_KEY:
            raise ImproperlyConfigured(self.name + ': EPAYCO_PUBLIC_KEY is not defined in your application\'s '
                                                   'settings. Please set your ePayco Account\'s Public Key before '
                                                   'using this package')

