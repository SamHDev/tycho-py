from __future__ import annotations
import typing

from .length import *
from .string import *


class Element:
    def validate(self, strict=True):
        pass

    def encode(self):
        return bytes()


class Unit(Element):
    def __init__(self):
        pass

    def encode(self):
        return bytes([0])


class Value(Element):
    def __init__(self, ident: int):
        self.ident = ident

    def encode(self):
        return bytes([16 + self.encode_prefix()]) + self.encode_body()

    def encode_prefix(self):
        return self.ident

    def encode_body(self):
        return bytes()


class Option(Element):
    def __init__(self, value: typing.Optional[Element]):
        self.value = value

    @property
    def is_some(self) -> bool:
        return self.value is not None

    @property
    def is_none(self) -> bool:
        return self.value is None

    def __repr__(self):
        return "Option(" + repr(self.value) + ")"

    def encode(self):
        if self.value is not None:
            return bytes([33]) + self.value.encode()
        else:
            return bytes([32])

    def __bool__(self):
        return self.is_some


class Array(Element):
    def __init__(self, data: typing.List[Element]):
        self.value = data

    def encode(self):
        build = bytes([48]) + encode_length(len(self.value))
        for key in self.value:
            build += key.encode()
        return build

    def __repr__(self):
        return "Array(" + repr(self.value) + ")"

    def __iter__(self):
        return self.value.__iter__()

    def __len__(self):
        return self.value.__len__()


class Structure(Element):
    def __init__(self, value: typing.Dict[str, Element]):
        self.value = value

    def keys(self) -> typing.List[str]:
        return [str(x) for x in self.value.keys()]

    def validate(self, strict=True):
        for key, value in self.value.items():
            if not (type(key) == str):
                raise KeyError(f"Key '{key}' is type {type(key)}, not str")
            if not isinstance(value, Element):
                raise ValueError(f"Value with key '{key}' is type {type(value)}, not Element")

    def __repr__(self):
        return "Structure(" + repr(self.value) + ")"

    def encode(self):
        build = bytes([64]) + encode_length(len(self.value))
        for key, value in self.value.items():
            build += encode_string(key)
            build += value.encode()
        return build

    def __iter__(self):
        return self.value.items().__iter__()

    def __len__(self):
        return self.value.__len__()


class Variant(Element):
    def __init__(self, name: str, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return "Variant(" + repr(self.name) + ", " + repr(self.value) + ")"

    def __len__(self):
        return self.value.__len__()

    def encode(self):
        return bytes([80]) + encode_string(self.name) + self.value.encode()


class Map(Element):
    def __init__(self, key_type: typing.Type[Value], data: typing.Dict[Element]):
        self.key_type = key_type
        self.value = data

    def validate(self, strict=True):
        i = 0
        value_type = None
        for key, value in self.value.items():
            if not isinstance(key, Value):
                raise KeyError(f"Key at index {i} is not a valid value ({type(key)})")
            elif not isinstance(key, self.key_type):
                raise KeyError(f"Key at index {i} does not match the parent key type")
            if strict:
                if value_type is None:
                    if not isinstance(value, Element):
                        raise ValueError("Value is not a valid element.")
                    value_type = type(value)
                elif value_type != type(value):
                    raise KeyError(f"Value at index {i} does not match the parent value type")
            i += 1

    def __repr__(self):
        return "Map(" + repr(self.key_type) + ", " + repr(self.value) + ")"

    def __len__(self):
        return self.value.__len__()

    def encode(self):
        build = bytes([80]) + encode_length(len(self.value))
        for key, value in self.value.items():
            build += key.encode_body()
            build += value.encode()
        return build

    def __iter__(self):
        return self.value.items().__iter__()


class List(Element):
    def __init__(self, item_type: typing.Type[Value], data: typing.List[Value]):
        self.item_type = item_type
        self.value = data

    def validate(self, strict=True):
        i = 0
        for item in self.value:
            if isinstance(item, self.item_type):
                raise ValueError(f"Item at index {i} is not of valid type")
            i += 1

    def encode(self):
        build = bytes([112 + self.item_type(0).encode_prefix()]) + encode_length(len(self.value))
        for key in self.value:
            build += key.encode_body()
        return build

    def __len__(self):
        return self.value.__len__()

    def __repr__(self):
        return "List(" + repr(self.item_type) + ", " + repr(self.value) + ")"

    def __iter__(self):
        return self.value.__iter__()
