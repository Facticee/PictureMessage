import getpass
import os

from rich import console
from rich.console import Console
from rich.panel import Panel

import crypto_handler
import image_embedder

console = Console()

def clean_path(path_str: str):
    return path_str.strip().strip('"').strip("'")

def verstecken():
    console.print(Panel("[bold cyan]Hide message in Image[/bold cyan]"))

    img_pfad = clean_path(input("Path to Image: "))
    if not os.path.exists(img_pfad):
        console.print("[red]No Image was found![/red]\n")
        return

    ziel_pfad = clean_path(input("Destination File (has to be PNG): "))
    if not  ziel_pfad.lower().endswith(".png"):
        ziel_pfad += ".png"

    text = input("Message: ").strip()
    if not text:
        console.print("[red]Message cant be empty[/red]")
        return

    pw = getpass.getpass("Password: ").strip()

    salt = os.urandom(16)
    secret_bytes = crypto_handler.verschlüsseln(text, pw, salt)

    binary = salt + secret_bytes

    yay = image_embedder.daten_verstecken(img_pfad, ziel_pfad, binary)
    if yay:
        console.print("[green] Message successfully hidden in Image [/green]")
    else:
        console.print("[red] Error while embedding the message. ")
        print("Please ensure the destination folder exists and the output file format is PNG.")


def auslesen():
    console.print(Panel("[bold yellow] Extracting Message[/bold yellow]"))

    img_pfad = clean_path(input("Path to Image: "))
    if not os.path.exists(img_pfad):
        print("[red]No Image was found![/red]")
        return

    pw = getpass.getpass("Password: ").strip()

    binary = image_embedder.extract_data(img_pfad)
    if binary is None:
        console.print("[red]No valid secrets found in Image[/red]")
        return

    salt = binary[:16]
    secret_bytes = binary[16:]

    text = crypto_handler.entschlüsseln(secret_bytes, pw, salt)
    if text is not None:
        print("-------------------------")
        print("Secret Message:", text)
        print("-------------------------")

    else:
        console.print("[red]Error while Extracting / Decrypting! Wrong password?[/red]")



while True:
    console.print("[bold magenta]---[ HiddenMessages ]---[/bold magenta]")
    console.print("1. Hide message in Image")
    console.print("2. Extract Message from Image")
    console.print("3. Close")

    wahl = input("Choice (1-3): ")

    if wahl == "1":
        verstecken()
    elif wahl == "2":
        auslesen()
    elif wahl == "3":
        print("Exit")
        break
    else:
        print("Invalid Choice! Choose 1, 2 or 3")