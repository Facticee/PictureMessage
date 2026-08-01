import getpass
import os

import crypto_handler
import image_embedder

def verstecken():
    print("HIDE MESSAGE")
    img_pfad = input("Path to image: ").strip().strip('"').strip('"')

    if os.path.exists(img_pfad):
        print("Image couldnt be found!")
        return

    ziel_pfad = input("Destination Image (has to be PNG): ").strip().strip('"').strip('"')
    if not ziel_pfad.lower().endswith('.png'):
        ziel_pfad += ".png"

    text = input("Messagee: ")
    pw = getpass.getpass("Password: ")

    salt = os.urandom(16)
    secret_bytes = crypto_handler.verschlüsseln(text, pw, salt)

    binary = salt + secret_bytes

    yay = image_embedder.daten_verstecken(img_pfad, ziel_pfad, binary)
    if yay:
        print("yay it worked")


def auslesen():
    print("Extract Message")
    img_pfad = input("Path to image: ").strip().strip('"').strip('"')

    if not os.path.exists(img_pfad):
        print("No Image could be found!")

    pw = getpass.getpass("Password: ")

    binary = image_embedder.extract_data(img_pfad)
    if binary is None:
        return

    salt = binary[:16]
    secret_bytes = binary[16:]

    text = crypto_handler.entschlüsseln(secret_bytes, pw, salt)
    if text is not None:
        print("-------------------------")
        print("Secret Message:", text)
        print("-------------------------")

while True:
    print("1. Hide message in Image")
    print("2. Extract Message from Image")
    print("3. Close")

    wahl = input("Choice (1-3): ")

    if wahl == "1":
        verstecken()
    elif wahl == "2":
        auslesen()
    elif wahl == "3":
        print("Exit")
        break
    else:
        print("Invalid Choice")