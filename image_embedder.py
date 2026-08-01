from sys import byteorder

import cv2
import numpy as np
from numpy.ma.core import shape, reshape


def bytes_zu_bits(data_bytes: bytes):
    return "".join(f"{b:08b}" for b in data_bytes)

def bits_to_bytes(bit_string: str):
    return bytes(int(bit_string[i : i + 8], 2) for i in range(0, len(bit_string), 8))



# final version (hoffentlich)
def daten_verstecken(image_path: str, output_path: str, binary_message: bytes):

    # loading image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Image couldnt be loaded under '{image_path}'")
        return False

    # putting message together
    data_length = len(binary_message)
    length_info = data_length.to_bytes(4, byteorder="big")
    full_message = length_info + binary_message

    # change to bit chain
    bit_chain = bytes_zu_bits(full_message)
    total_bits = len(bit_chain)

    # checking if image is big enough
    flat_img = img.flatten()
    if total_bits > flat_img.size:
        print(f"Image is too small - Available: {flat_img.size} Bits, Needed: {total_bits} Bits")
        return False

    for i in range(total_bits):
        pixel = flat_img[i]
        ziel_bit = int(bit_chain[i]) # 0 or 1
        flat_img[i] = (pixel - (pixel % 2)) + ziel_bit

    secret_image = flat_img.reshape(img.shape)

    if cv2.imwrite(output_path, secret_image):
        print(f"Image was saved under '{output_path}'")
        return True
    else:
        print(f"Error while saving under '{output_path}'")
        print("Please ensure the destination folder exists and the output file format is PNG.")
        return False


if __name__ == "__main__":

    test_bild = np.zeros((100, 100, 3), dtype=np.uint8)
    test_bild[:] = (255, 0, 0)
    cv2.imwrite("test_input.png",test_bild)

    secretmessage = "SecretMessage123!".encode("utf-8")

    idk = daten_verstecken(image_path="test_input.png", output_path="test_output.png", binary_message=secretmessage,)

    if idk:
        print("YAY")

