from django.conf import settings
from .encryption import Crypto
import requests


class ePaycoBasicTransactionObjet(object):

    metodoconfirmacion = 'POST' # Could also be GET
    lenguaje = 'python'

    def __init__(self, **kwargs):
        self.ip = kwargs.get('ip')
        self.tipo_doc = kwargs.get('tipo_doc')
        self.documento = kwargs.get('documento')
        self.fechaExpedicion = kwargs.get('fechaExpedicion')
        self.nombres = kwargs.get('nombres')



class ePaycoConnector(object):
    """
    This class implements all connection methods with ePayco. Since ePayco is a REST API, it makes sense not to
    instantiate this class and simply have static methods all over the place
    """

    @classmethod
    def request(cls, payload, url, method):
        """
        This helper method infuses a request to ePayco with all necessary authentication parameters (properly encrypted) and
        also marks the call as a Test call according to the application's settings

        :param payload: The object representing this
        :param url: url to be requested
        :param method: 'get' or 'post' according to the type of request you're doing to ePayco's API.
        :return: ePayco's response, in a requests.response object
        """

        cryptograph = Crypto()

        setattr(payload, 'public_key', settings.EPAYCO_PUBLIC_KEY)
        setattr(payload, 'i', cryptograph.get_initialization_vector())
        setattr(payload, 'lenguaje', 'python')
        if settings.EPAYCO_TEST_ENVIRONMENT:
            setattr(payload, 'enpruebas', settings.EPAYCO_TEST_ENVIRONMENT)
        response = requests.request(method, url, data=payload)
        # TODO: Do some post processing here? AKA general error handling?
        return response


