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
    telefono = forms.CharField(required=False)
    celular = forms.CharField(required=False)
    ip = forms.IPAddressField(required=True)
    direccion = forms.CharField(required=True)
    pais = forms.CharField(max_length=2, required=True)

    # Invoicing information
    factura = forms.CharField(required=True)
    descripcion = forms.CharField(required=True)
    iva = forms.CharField(required=True, initial="0")
    baseiva = forms.CharField(required=True, initial="0")
    valor = forms.CharField(required=True)
    moneda = forms.CharField(min_length=3, max_length=3, required=True, initial='COP')

    # authentication data
    public_key = forms.CharField(required=True, initial=settings.EPAYCO_PUBLIC_KEY)
    i = forms.CharField(max_length=100, required=True)
    enpruebas = forms.BooleanField(required=True, initial=settings.EPAYCO_TEST_ENV)

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

    def __init__(self, *args, **kwargs):
        if 'data' in kwargs:
            crypto = Crypto()

            kwargs.get('data').update({
                'i': crypto.base_64_encode(crypto.get_initialization_vector()),
                'enpruebas': settings.EPAYCO_TEST_ENV,
                'public_key': settings.EPAYCO_PUBLIC_KEY
            })
        super(EpaycoBaseForm, self).__init__(*args, **kwargs)

    def encode_data(self):
        if not self.is_valid():
            print(self.errors)
            # raise Exception('Form data has not been cleared. Please use full_clean() before calling this method ')
        crypto = Crypto()
        iv = crypto.base_64_decode(self.cleaned_data.get('i'))
        for key, value in self.cleaned_data.items():
            if key != 'i':
                # we encrypt everything but the initialization vector
                self.cleaned_data[key] = str(crypto.encrypt(str(value), iv).get('content'))
        return self.cleaned_data


