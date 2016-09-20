"""
Settings for django-epayco
"""
from django.conf import settings

"""
This is the private key of your ePayco account
"""
EPAYCO_PRIVATE_KEY = getattr(settings, 'EPAYCO_PRIVATE_KEY', None)

"""
This is the public key of the ePayco account
"""
EPAYCO_PUBLIC_KEY = getattr(settings, 'EPAYCO_PUBLIC_KEY', None)

"""
This flag tells us to use test calls instead of actual production calls to ePayco (good for testing, prototyping and pre-production stages
"""
EPAYCO_TEST_ENV = getattr(settings, 'EPAYCO_TEST_ENV', False)

