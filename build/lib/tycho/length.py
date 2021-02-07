from io import BytesIO


def encode_length(n: int):
    if n < 0:
        raise ValueError("Length is less than 0")
    elif n < 0x3F:
        return (n & 0x3F).to_bytes(1, "big")
    elif n < 0x3FFF:
        return ((n & 0x3FFF) + 0x4000).to_bytes(2, "big")
    elif n < 0x3FFFFF:
        return ((n & 0x3FFFFF) + 0x800000).to_bytes(3, "big")
    elif n < 0x3FFFFFFF:
        return ((n & 0x3FFFFFFF) + 0xc0000000).to_bytes(4, "big")
    else:
        raise ValueError("Length is larger than (2^30)-1")


def decode_length(r: BytesIO):
    leading = r.read(1)[0]
    size = int(leading) >> 6
    read = bytes([leading & 0x3F]) + r.read(size)
    return int.from_bytes(read, "big")

