import io


def hex_to_bytes(hex_str):
    bytes = []
    hex_str = ''.join(hex_str.split(' '))

    for i in range(0, len(hex_str), 2):
        bytes.append(int(hex_str[i:i + 2], 16))
    return bytes


def hex_to_stream(hex_str):
    barr = bytearray.fromhex(hex_str)
    return io.BytesIO(barr)
