from __future__ import annotations
import typing

from .elements import Value, encode_string
from .length import encode_length
import struct


class Boolean(Value):
    value: bool

    def __init__(self, value: bool):
        super().__init__(0)
        self.value = value

    def __repr__(self):
        return "Boolean(" + repr(self.value) + ")"

    def __str__(self):
        return self.value

    def __bool__(self):
        return self.value

    def encode_body(self):
        return bytes([int(self.value)])


class NumericalValue(Value):
    value: int

    def __init__(self, value: int, _min: int, _max: int, byte_size: int, signed: bool, ident: int):
        super().__init__(ident)
        self.value = value
        self.byte_size = byte_size
        self.signed = signed
        if _min >= value or _max <= value:
            raise ValueError(f"Value {value} is out of bounds ({_min}-{_max})")

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.value) + ")"

    def __str__(self):
        return self.value

    def __bool__(self):
        return self.value

    def __int__(self):
        return self.value

    def __float__(self):
        return float(self.value)

    def encode_body(self):
        return self.value.to_bytes(self.byte_size, "big", signed=self.signed)


class Unsigned8(NumericalValue):
    def __init__(self, value: int):
        super().__init__(value, 0, 0xFF, 1, False, 1)


class Unsigned16(NumericalValue):
    def __init__(self, value: int):
        super().__init__(value, 0, 0xFFFF, 2, False, 2)


class Unsigned32(NumericalValue):
    def __init__(self, value: int):
        super().__init__(value, 0, 0xFFFFFFFF, 4, False, 3)


class Unsigned64(NumericalValue):
    def __init__(self, value: int):
        super().__init__(value, 0, 0xFFFFFFFFFFFFFFFF, 8, False, 4)


class Unsigned128(NumericalValue):
    def __init__(self, value: int):
        super().__init__(value, 0, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF, 16, False, 5)


class Signed8(NumericalValue):
    def __init__(self, value: int):
        super().__init__(value, -0x8F, 0x8F, 1, True, 6)


class Signed16(NumericalValue):
    def __init__(self, value: int):
        super().__init__(value, -0x8FFF, 0x8FFF, 2, True, 7)


class Signed32(NumericalValue):
    def __init__(self, value: int):
        super().__init__(value, -0x8FFFFFFF, 0x8FFFFFFF, 4, True, 8)


class Signed64(NumericalValue):
    def __init__(self, value: int):
        super().__init__(value, -0x8FFFFFFFFFFFFFFFFF, 0x8FFFFFFFFFFFFFFFFF, 8, True, 9)


class Signed128(NumericalValue):
    def __init__(self, value: int):
        super().__init__(value, -0x8FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF, 0x8FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF, 16, True,
                         10)


class Float32(Value):
    def __init__(self, value: float):
        super().__init__(11)
        self.value = value

    def encode_body(self):
        return struct.pack('>f', self.value)

    def __repr__(self):
        return f"Float32({self.value})"

    def __str__(self):
        return str(self.value)

    def __float__(self):
        return self.value

    def __int__(self):
        return int(self.value)


class Float64(Value):
    def __init__(self, value: float):
        super().__init__(12)
        self.value = value

    def encode_body(self):
        return struct.pack('>d', self.value)

    def __repr__(self):
        return f"Float64({self.value})"

    def __str__(self):
        return str(self.value)

    def __float__(self):
        return self.value

    def __int__(self):
        return int(self.value)


class Char(Value):
    value: str

    def __init__(self, value: str):
        super().__init__(13)
        self.value = value

    def validate(self, strict=True):
        if len(self.value) != 1:
            raise ValueError("Value is not a char (length != 1)")

    def __repr__(self):
        return "String(" + repr(self.value) + ")"

    def __str__(self):
        return self.value

    def __len__(self):
        return len(self.value)

    @property
    def length(self) -> int:
        return len(self.value)

    @property
    def byte_length(self) -> int:
        return len(self.value.encode("utf-8"))

    def encode_body(self):
        data = self.value.encode("utf-8")
        return encode_length(len(data)) + data

    def __iter__(self):
        return self.value.__iter__()


class String(Value):
    value: str

    def __init__(self, value: str):
        super().__init__(14)
        self.value = value

    @property
    def length(self) -> int:
        return len(self.value)

    @property
    def byte_length(self) -> int:
        return len(self.value.encode("utf-8"))

    def __len__(self):
        return len(self.value)

    def __repr__(self):
        return "String(" + repr(self.value) + ")"

    def __str__(self):
        return self.value

    def encode_body(self):
        return encode_string(self.value)

    def __iter__(self):
        return self.value.__iter__()


class Bytes(Value):
    value: bytes

    def __init__(self, value: bytes):
        super().__init__(15)
        self.value = value

    @property
    def length(self) -> int:
        return len(self.value)


    @staticmethod
    def from_list(data: typing.Iterable[int]):
        i = 0
        for byte in data:
            if not (0 <= byte < 256):
                raise ValueError(f"Value at index {i} is not a valid byte. ({byte})")
            i += 1
        return Bytes(bytes(data))

    def __repr__(self):
        return "Bytes(" + str(self.value) + ")"

    def encode_body(self):
        return encode_length(len(self.value)) + self.value

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        return self.value.__iter__()
