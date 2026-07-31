import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def get_key(pw, salt):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
    return base64.urlsafe_b64encode(kdf.derive(pw.encode()))

def verschlüsseln(text, pw, salt):
    f = Fernet(get_key(pw, salt))
    res = f.encrypt(text.encode())
    return res

def entschlüsseln(data, pw, salt):
    try:
        f = Fernet(get_key(pw, salt))
        return f.decrypt(data).decode()
    except:
        print("Error while decrypting!")
        return None

if __name__ == "__main__":

    passwort = "MyPassword"
    secret = "Hello World"

    salt = os.urandom(16)

    print(" DE- ENCRYPTION TEST")
    print(f"Pre encrypted: {secret}")

    verschlüsselt = verschlüsseln(secret, passwort, salt)
    print(f"encrypted {verschlüsselt}")

    entschlüsselt = entschlüsseln(verschlüsselt, passwort, salt)
    print(f"Decrypted: {entschlüsselt}")

