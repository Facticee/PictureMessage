import base64
import os

from cryptography import fernet
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def get_key(pw, salt):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
    return base64.urlsafe_b64encode(kdf.derive(pw.encode()))

def verschlüsseln(message: str, pw: str, salt: bytes):
    key = get_key(pw, salt)
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())

def entschlüsseln(encrypted_bytes: bytes, pw: str, salt: bytes):
    key = get_key(pw, salt)
    fernet = Fernet(key)
    try:
        return fernet.decrypt(encrypted_bytes).decode()
    except InvalidToken:
        print("Decryption Failed: Incorrect password?")
        return None
if __name__ == "__main__":

    passwort = "MyPassword"
    secret = "Hello World"

    salt = os.urandom(16)

    print(" DE- ENCRYPTION TEST")
    print(f"Pre Encryption: {secret}")

    verschlüsselt = verschlüsseln(secret, passwort, salt)
    print(f"Encrypted {verschlüsselt}")

    entschlüsselt = entschlüsseln(verschlüsselt, passwort, salt)
    print(f"Decrypted: {entschlüsselt}")

    print("Test with wrong password:")
    entschlüsseln(verschlüsselt, "WrongMyPassword", salt)
