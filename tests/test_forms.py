from django.test import TestCase
from django_epayco import forms, encryption
from django.conf import settings


class TestBaseFormEncoding(TestCase):

    def get_test_data(self):

        return {
            "tipo_doc": "CC",
            "documento": "123456789",
            "fechaExpedicion": "2005-01-01",
            "nombres":  "Camilo",
            "apellidos": "Díaz",
            "email": "cliente@cliente.com",
            "pais": "CO",
            "depto": "Antioquia",
            "ciudad": "Medellín",
            "telefono": "4365234",
            "celular": "0000000000",
            "direccion": "Calle 67 # 23 - 22",
            "ip": "186.116.10.133",
            "factura": "43256",
            "descripcion": "Nuevo pago de 20.000",
            "iva": "0",
            "baseiva": "0",
            "valor": "20000",
            "moneda": "COP",
            "url_respuesta": "https://www.epayco.co/respuesta",
            "url_confirmacion": "https://www.epayco/callback",
            "metodoconfirmacion": "POST",
            "lenguaje": "php"
        }

    def test_form_encodes_expected(self):

        crypto = encryption.Crypto(settings.EPAYCO_PRIVATE_KEY)  # crypto instance for checkings
        testForm = forms.EpaycoBaseForm(data=self.get_test_data())  # our test form, initialized with our test data
        testForm.full_clean()  # clean the form, this should validate it.
        encodedData = testForm.encode_data()  # encode data
        iv = crypto.base_64_decode(encodedData.get('i'))  # get get the encoded data's Init. vector for our assertions

        for key, value in self.get_test_data().items():
            # We assert the values passed are properly encoded
            encrypted_value = crypto.encrypt(str(value), iv).decode('utf-8')
            self.assertEqual(
                str(encrypted_value),
                encodedData.get(key),
                'Encoded data for ' + key + ' did not match expected value. Expected: ' + str(encrypted_value) + ' but got ' +
                str(encodedData.get(key)))


class TestCreditCardFormFields(TestCase):
    """
    This class tests the fields for a credit card request are correctly processed.
    """

    def get_test_data(self):
        return {
           "tipo_doc": "CC",
           "documento": "123456789",
           "fechaExpedicion": "2005-01-01",
           "nombres":  "Camilo",
           "apellidos": "Díaz",
           "email": "cliente@cliente.com",
           "pais": "CO",
           "depto": "Antioquia",
           "ciudad": "Medellín",
           "telefono": "4365234",
           "celular": "0000000000",
           "direccion": "Calle 67 # 23 - 22",
           "ip": "186.116.10.133",
           "factura": "43256",
           "descripcion": "Nuevo pago de 20.000",
           "iva": "0",
           "baseiva": "0",
           "valor": "20000",
           "moneda": "COP",
           "tarjeta": "4575623182290326",
           "fechaexpiracion": "2018-06",
           "codigoseguridad": "123",
           "franquicia": "VISA",
           "cuotas": "1",
           "url_respuesta": "https://www.epayco.co/respuesta",
           "url_confirmacion": "https://www.epayco/callback",
           "metodoconfirmacion": "POST",
           "lenguaje": "php"
        }

    def test_credit_card_form_valid(self):
        testForm = forms.EpaycoCreditCardForm(data=self.get_test_data())  # our test form, initialized with our test data
        testForm.full_clean()  # clean the form, this should validate it.
        self.assertTrue(testForm.is_valid(), 'Credit card form is invalid for test dataset ' + str(testForm.errors))

