from Crypto.Cipher import AES
from Crypto import Random
import base64


class Crypto(object):

    mode = AES.MODE_CBC

    def __init__(self, key):
        self.key = key

    def encrypt(self, content, iv=None):
        """
        This method encrypts whatever is contained in content according to ePayco's API encryption requirements and
        returns it. the parameter is left unmodified
        The encryption method used is AES128 in CBC mode with a PKCS7 padding
        :param content: A string to be encrypted
        :param iv: random 16 bits initialization vector. can usually be the result of get_initialization_vector
        :return: an bytearray with the encrypted data
        """
        if not iv:
            iv = self.get_initialization_vector() # store the iv for later use and return
        encryptor = AES.new(self.key, self.mode, iv)

        return base64.b64encode(encryptor.encrypt(self.pkcs7(content)))

    def get_initialization_vector(self):
        """
        This method returns the initialization vector required by ePayco's API. According to the API's specs, it is
        built based on the following concepts:
        - not encrypted
        - 16 bytes long
        :return:
        """
        return Random.new().read(AES.block_size)

    def pkcs7(self, s):
        """
        Applies a pkcs7 padding to plaintext
        :param data:
        :return:
        """
        # calculate the padding length. string is encoded to prevent special characters to destruct our count
        length = AES.block_size - (len(s.encode('utf-8')) % AES.block_size)
        # add as many bytes as needed
        s += chr(length)*length
        return s

    def base_64_encode(self, s):
        return base64.b64encode(s)

    def base_64_decode(self, s):
        return base64.b64decode(s)


