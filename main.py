import getpass
import os

from rich import console
from rich.console import Console
from rich.panel import Panel

import crypto_handler
import image_embedder

def clean_path(path_str: str):
    return path_str.strip().strip('"').strip("'")

def verstecken():
    print("[bold cyan] Hide message in Image [/bold cyan]")
    img_pfad = clean_path(input("Path to Image: "))
    if not os.path.exists(img_pfad):
        console.print("[red] No Image was found! [/red]")


    ziel_pfad = clean_path(input("Destination File (has to be PNG): "))
    if not  ziel_pfad.lower().endswith(".png"):
        ziel_pfad += ".png"

    text = input("Message: ").strip()
    pw = getpass("Password: ").strip()

    if not text:
        print("Message cannot be empty!")

    if not pw:
        print("Password cannot be empty!")


    salt = os.urandom(16)
    secret_bytes = crypto_handler.verschlüsseln(text, pw, salt)

    binary = salt + secret_bytes

    yay = image_embedder.daten_verstecken(img_pfad, ziel_pfad, binary)
    if yay:
        print("TEST")


def auslesen():
    print("--- Extract Message ---")
    img_pfad = clean_path(input("Path to Image: "))

    if not os.path.exists(img_pfad):
        print("No Image was found!")
        return

    pw = getpass.getpass("Password: ").strip()

    binary = image_embedder.extract_data(img_pfad)
    if binary is None:
        return

    salt = binary[:16]
    secret_bytes = binary[16:]

    text = crypto_handler.entschlüsselt(secret_bytes, pw, salt)
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