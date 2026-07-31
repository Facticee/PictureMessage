

def bytes_zu_bits(data_bytes: bytes):
    return "".join(f"{b:08b}" for b in data_bytes)

def bits_to_bytes(bit_string: str):
    return bytes(int(bit_string[i : i + 8], 2) for i in range(0, len(bit_string), 8))


