from django.core import validators
from django import forms
from django.conf import settings
from .encryption import Crypto


class AESEncryptedField(forms.CharField):
    def __init__(self, max_length=None, min_length=None, iv=None, *args, **kwargs):
        if iv:
            self.iv = iv
        else:
            self.iv = Crypto().get_initialization_vector()
        super(AESEncryptedField, self).__init__(max_length, min_length, *args, **kwargs)


class EpaycoBaseForm(forms.Form):
    """
    Forms are used mainly for data validation
    """

    # Personal information
    tipo_doc = forms.CharField(required=True)
    documento = forms.CharField(required=True)
    fechaExpedicion = forms.CharField(required=False, initial='')
    nombres = forms.CharField(required=True)
    apellidos = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    depto = forms.CharField(required=False)
    ciudad = forms.CharField(required=True)
    telefono = forms.IntegerField(max_value=9999999, required=False)
    celular = forms.IntegerField(max_value=9999999999)
    ip = forms.IPAddressField(required=True)

    # Invoicing information
    factura = forms.CharField(required=True)
    descripcion = forms.CharField(required=True)
    iva = forms.FloatField(required=True, initial=0)
    baseiva = forms.FloatField(required=True, initial=0)
    valor = forms.FloatField(required=True)
    moneda = forms.CharField(min_length=3, max_length=3, required=True, initial='COP')

    # authentication data
    public_key = forms.CharField(required=True, initial=settings.EPAYCO_PUBLIC_KEY)
    i = forms.CharField(max_length=16, required=True)
    enpruebas = forms.BooleanField(required=True, initial=settings.EPAYCO_TEST_ENVIRONMENT)

    # Response handling communication
    url_respuesta = forms.URLField(required=True)
    url_confirmacion = forms.URLField(required=True)
    metodoconfirmacion = forms.ChoiceField(
        choices=(
            ('POST', 'POST'),
            ('GET', 'GET')
        ),
        required=True
    )

    # Language... not sure why?
    lenguaje = forms.CharField(initial='python', required=True)

    def encode_data(self):
        if not self.is_valid():
            raise Exception('Form data has not been cleared. Please use full_clean() before calling this method ')
        crypto = Crypto()
        iv = crypto.get_initialization_vector()
        for key, value in self.cleaned_data:
            if key != 'i':
                # we encrypt everything but the initialization vector
                self.cleaned_data[key] = str(crypto.encrypt(self.cleaned_data[key], iv).get('content'))
        return self.cleaned_data


