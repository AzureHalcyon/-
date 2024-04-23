# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import padding
# import base64
# import random
# import string
# '''
# function getAesString(data, key0, iv0) {
#     key0 = key0.replace(/(^\s+)|(\s+$)/g, "");
#     var key = CryptoJS.enc.Utf8.parse(key0);
#     var iv = CryptoJS.enc.Utf8.parse(iv0);
#     var encrypted = CryptoJS.AES.encrypt(data, key, {
#         iv: iv,
#         mode: CryptoJS.mode.CBC,
#         padding: CryptoJS.pad.Pkcs7
#     });
#     return encrypted.toString();
# }
# function encryptAES(data, aesKey) {
#     if (!aesKey) {
#         return data;
#     }
#     var encrypted = getAesString(randomString(64) + data, aesKey, randomString(16));
#     return encrypted;
# }
# var $aes_chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';
# var aes_chars_len = $aes_chars.length;
# function randomString(len) {
#     var retStr = '';
#     for (i = 0; i < len; i++) {
#         retStr += $aes_chars.charAt(Math.floor(Math.random() * aes_chars_len));
#     }
#     return retStr;
# }'''
# def getAesString(data, key0, iv0):
#     """
#     Encrypts the input data using the AES algorithm with the provided key and IV.

#     Args:
#         data (str): The data to be encrypted.
#         key0 (str): The key used for encryption.
#         iv0 (str): The initialization vector used for encryption.

#     Returns:
#         str: The base64 encoded encrypted data.
#     """
#     key0 = key0.strip()
#     key = key0.encode('utf-8')
#     iv = iv0.encode('utf-8')
    
#     padder = padding.PKCS7(algorithms.AES.block_size).padder()
#     padded_data = padder.update(data.encode('utf-8')) + padder.finalize()

#     cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
#     encryptor = cipher.encryptor()
#     encrypted = encryptor.update(padded_data) + encryptor.finalize()

#     return base64.b64encode(encrypted).decode('utf-8')
# def encryptAes(data, aes_key):
#     """
#     Login Encrypts the input data using the AES algorithm with the provided key.
#     Encrypts the given data using AES encryption.

#     Args:
#         data: The data to be encrypted.
#         aes_key: The AES encryption key.

#     Returns:
#         str: The encrypted data.
#     """
#     if not aes_key:
#         return data
#     random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
#     data_to_encrypt = random_str + data

#     encrypted = getAesString(data_to_encrypt, aes_key, ''.join(random.choices(string.ascii_letters + string.digits, k=16)))
#     return encrypted

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import base64
import random
import string

def getAesString(data, key0, iv0):
    """
    Encrypts the input data using the AES algorithm with the provided key and IV.

    Args:
        data (str): The data to be encrypted.
        key0 (str): The key used for encryption.
        iv0 (str): The initialization vector used for encryption.

    Returns:
        str: The base64 encoded encrypted data.
    """
    key0 = key0.strip()
    key = key0.encode('utf-8')
    iv = iv0.encode('utf-8')
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(data.encode('utf-8'), AES.block_size)

    encrypted = cipher.encrypt(padded_data)

    return base64.b64encode(encrypted).decode('utf-8')

def encryptAes(data, aes_key):
    """
    Encrypts the input data using the AES algorithm with the provided key.

    Args:
        data: The data to be encrypted.
        aes_key: The AES encryption key.

    Returns:
        str: The encrypted data.
    """
    if not aes_key:
        return data
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
    data_to_encrypt = random_str + data

    iv = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    encrypted = getAesString(data_to_encrypt, aes_key, iv)
    return encrypted
