from .length import *
from io import BytesIO


def encode_string(s: str):
    data = s.encode("utf-8")
    return encode_length(len(data)) + data


def decode_string(io: BytesIO):
    length = decode_length(io)
    return io.read(length).decode("utf-8")
