from django.test import TestCase
from django_epayco import encryption


"""
This file will test encryption properties of our encryption library
"""


class EncryptedDataSucceeds(TestCase):
    def test_encrypted_data_matches_examples(self):
        crypto = encryption.Crypto()

        iv = crypto.base_64_decode('MDAwMDAwMDAwMDAwMDAwMA==')
        cellphone = "0000000000"
        dept = "Antioquia"
        description = "Nuevo pago de 20.000"

        encrypted_data = {
            'cellphone': crypto.encrypt(cellphone, iv),
            'dept': crypto.encrypt(dept, iv),
            'description': crypto.encrypt(description, iv)
        }

        test_encrypted_data = {
            'cellphone': 'MgX2/Rg9IhsIclrR6rBcPw==',
            'dept': 'b9WzUeEU+5dqTU+kUEC29A==',
            'description': 'HrjCJyRqc+PIniCs2cJodEoiJrP3iXHszYhAZowCuNQ='
        }

        for key, value in encrypted_data.items():
            self.assertEqual(value.get('content'), test_encrypted_data.get(key), str(crypto.__class__) +
                             ' : Not correctly encrypted. Expected: ' + str(test_encrypted_data.get(key)) +
                             ' but got: ' + str(value.get('content')))


class EncryptedDataFails(TestCase):
    """
    This test class will test if the encryption is different given different parameters
    """
    def test_encrypted_data_does_not_match_examples(self):
        crypto = encryption.Crypto()

        iv = crypto.get_initialization_vector()
        cellphone = "0000000000"
        dept = "Antioquia"
        description = "Nuevo pago de 20.000"

        encrypted_data = {
            'cellphone': crypto.encrypt(cellphone, iv),
            'dept': crypto.encrypt(dept, iv),
            'description': crypto.encrypt(description, iv)
        }

        test_encrypted_data = {
            'cellphone': b'MgX2/Rg9IhsIclrR6rBcPw==',
            'dept': b'b9WzUeEU+5dqTU+kUEC29A==',
            'description': b'HrjCJyRqc+PIniCs2cJodEoiJrP3iXHszYhAZowCuNQ='
        }

        for key, value in encrypted_data.items():
            self.assertNotEqual(value.get('content'), test_encrypted_data.get(key), str(crypto.__class__) +
                                ' : Not correctly encrypted. Expected: ' + str(test_encrypted_data.get(key)) +
                                ' but got: ' + str(value.get('content')))


class InitializationVectorAlwaysDifferent(TestCase):

    def test_initialization_vector_different(self):
        """
        this method will test if the initialization vector provided by this library is at least consistently different
        with each time we generate it

        :return:
        """
        crypto = encryption.Crypto()
        iv1 = crypto.get_initialization_vector()
        iv2 = crypto.get_initialization_vector()
        self.assertNotEqual(iv1, iv2, 'Initialization vectors should not be equals')


