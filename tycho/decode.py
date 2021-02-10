from io import BytesIO

from tycho.elements import *
from tycho.values import *


def decode(b: bytes) -> Element:
    data = BytesIO(b)
    return decode_element(data)


def decode_element(data: BytesIO) -> Element:
    prefix = data.read(1)[0]
    element_type = prefix >> 4
    element_data = prefix & 0xF

    if element_type == 0:
        return Unit()

    elif element_type == 1:
        return decode_value(data, element_data)

    elif element_type == 2:
        if element_data == 0x00:
            return Option(None)
        else:
            return Option(decode_element(data))

    elif element_type == 3:
        length = decode_length(data)
        build = []
        for _i in range(0, length):
            build.append(decode_element(data))
        return Array(build)

    elif element_type == 4:
        length = decode_length(data)
        build = {}
        for _i in range(0, length):
            key = decode_string(data)
            value = decode_element(data)
            build[key] = value
        return Structure(build)

    elif element_type == 5:
        name = decode_string(data)
        value = decode_element(data)
        return Variant(name, value)

    elif element_type == 6:
        length = decode_length(data)
        build = {}
        for _i in range(0, length):
            key = decode_value(data, element_data)
            value = decode_element(data)
            build[key] = value
        return Map(get_element_type_from_ident(element_data), build)

    elif element_type == 7:
        length = decode_length(data)
        build = []
        for _ in range(0, length):
            build.append(decode_value(data, element_data))
        return List(get_element_type_from_ident(element_data), build)


def decode_value(data: BytesIO, typed) -> Value:
    if typed == 0:
        return Boolean(data.read(1)[0] == 0x01)
    elif typed == 1:
        return Unsigned8(int.from_bytes(data.read(1), "big", signed=False))
    elif typed == 2:
        return Unsigned16(int.from_bytes(data.read(2), "big", signed=False))
    elif typed == 3:
        return Unsigned32(int.from_bytes(data.read(4), "big", signed=False))
    elif typed == 4:
        return Unsigned64(int.from_bytes(data.read(8), "big", signed=False))
    elif typed == 5:
        return Unsigned128(int.from_bytes(data.read(16), "big", signed=False))
    elif typed == 6:
        return Signed8(int.from_bytes(data.read(1), "big", signed=True))
    elif typed == 7:
        return Signed16(int.from_bytes(data.read(2), "big", signed=True))
    elif typed == 8:
        return Signed32(int.from_bytes(data.read(4), "big", signed=True))
    elif typed == 9:
        return Signed64(int.from_bytes(data.read(8), "big", signed=True))
    elif typed == 10:
        return Signed128(int.from_bytes(data.read(16), "big", signed=True))
    elif typed == 11:
        return Float32(struct.unpack(">f", data.read(4))[0])
    elif typed == 12:
        return Float32(struct.unpack(">d", data.read(8))[0])
    elif typed == 14:
        size = decode_length(data)
        s = data.read(size).decode("utf-8")
        return Char(s[0])
    elif typed == 13:
        return String(decode_string(data))
    elif typed == 15:
        size = decode_length(data)
        return Bytes(data.read(size))
    else:
        raise ValueError(f"Failed to decode value with type ident {typed}")


def get_element_type_from_ident(ident):
    if ident == 0:
        return Boolean
    elif ident == 1:
        return Unsigned8
    elif ident == 2:
        return Unsigned16
    elif ident == 3:
        return Unsigned32
    elif ident == 4:
        return Unsigned64
    elif ident == 5:
        return Unsigned128
    elif ident == 6:
        return Signed8
    elif ident == 7:
        return Signed16
    elif ident == 8:
        return Signed32
    elif ident == 9:
        return Signed64
    elif ident == 10:
        return Signed128
    elif ident == 11:
        return Float32
    elif ident == 12:
        return Float32
    elif ident == 13:
        return Char
    elif ident == 14:
        return String
    elif ident == 15:
        return Bytes
    else:
        raise ValueError(f"Cannot get type from ident {ident}")
