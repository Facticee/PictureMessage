from sys import byteorder

import cv2
import numpy as np
from numpy.ma.core import shape, reshape


def bytes_zu_bits(data_bytes: bytes):
    return "".join(f"{b:08b}" for b in data_bytes)

def bits_to_bytes(bit_string: str):
    return bytes(int(bit_string[i : i + 8], 2) for i in range(0, len(bit_string), 8))









# version 1 von nachricht da drin packen ins bild
def daten_verstecken(bild_pfad, ziel_pfad, daten):
    img = cv2.imread(bild_pfad)
    if img is None:
        print("No Image was found!")
        return False

    länge = len(daten)
    header = länge.to_bytes(4, byteorder="big")
    gesamt_daten = header + daten

    bits = bytes_zu_bits(gesamt_daten)

    flat = img.flatten()
    if len(bits) > len(flat):
        print("Image is too small ")
        return False

    for i in range(len(bits)):
        if bits[i] == "1":
            flat[i] = flat[i] | 1
        else:
            flat[i] = flat[i] & 254

    neues_bild = flat.reshape(img.shape)

    return True

# Version 3 final
def embed_data(image_path: str, ziel_pfad: str, daten: bytes):

    img = cv2.imread(image_path)
    if img is None:
        print(f"No Image found under '{image_path}'")
        return False

    data_length = len(daten)
    header = data_length.to_bytes(4)
    gesamte_daten = header + data_length

    bit_chain = bytes_zu_bits(gesamte_daten)
    anzahl_bits = len(bit_chain)

    flat_img = img.flatten()
    if anzahl_bits > len(flat_img):
        print("Image too small for the message")
        return False

    for i in range(anzahl_bits):
        if anzahl_bits[i] == 1:
            flat_img[i] = flat_img[i] | 1
        else:
            flat_img[i] = flat_img[i] & 254

    neues_bild = flat_img.reshape(img.shape)
    cv2.imwrite(ziel_pfad, neues_bild)
    print(f"Saved in {ziel_pfad}")
    return True


# version 2 von nachricht da drin ins bild packen XXXXXXXXXXXXXXXXXXXXXXXXXXX

def embed_data(image_path: str, output_path: str, binary_message: bytes):
    img = cv2.imread(image_path)
    if img is None:
        print("Couldnt load input image!")
        return False

    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(
            "Couldnt load input image!"
        )

    data_length = len(binary_message)
    length_bytes = data_length.to_bytes(4, byteorder="big")
    full_binary_message = length_bytes + binary_message

    bit_stream = bytes_zu_bits(full_binary_message)
    total_bits = len(bit_stream)

    #test

    flat_img = img.flatten()
    if total_bits > flat_img.size:
        raise ValueError(f"Image capacity exceeded! Needs: {total_bits} - Available {flat_img.size} ")

    #test

    total_pixels = img.shape[0] * img.shape[1] * img.shape[2]
    if total_pixels > total_bits:
        raise ValueError(
            "The Image is too small"
        )

    flat_img = img.flatten()
    for i in range(total_bits):
        flat_img[i] = (flat_img & 0xFE) | int(bit_stream[i])

    reshaped_img = flat_img.reshape(img.shape)

    return True


