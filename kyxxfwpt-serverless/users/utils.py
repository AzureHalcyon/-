import os
from cryptography.fernet import Fernet

key = os.environ.get("MY_SECRET_KEY")
key = "lT7f2p0EpLOgivgffilEOCbnAsYZmvcalF0MKw1gSzc="
cipher_suite = Fernet(key)


# encrypted_password = cipher_suite.encrypt(password.encode())
# decrypted_password = cipher_suite.decrypt(encrypted_password).decode()