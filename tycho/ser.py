from .elements import *
from .values import *

from typing import Optional, Type


def serialise(t) -> Element:
    if isinstance(t, dict):
        if is_structure(t):
            return Structure({str(key): serialise(value) for key, value in t.items()})
        map_type = find_array_type(t.keys())
        if map_type is None:
            return Structure({str(key): serialise(value) for key, value in t.items()})
        else:
            return Map(map_type, {serialise_value(key): serialise(value) for key, value in t.items()})
    elif isinstance(t, list) or isinstance(t, tuple):
        list_type = find_array_type(t)
        if list_type is None:
            return Array([serialise(x) for x in list(t)])
        else:
            return List(list_type, [serialise_value(x, typed=list_type) for x in list(t)])
    elif t is None:
        return Option(None)
    else:
        v = serialise_value(t)
        if v is None:
            raise ValueError("Unserializable value parsed")
        else:
            return v


def serialise_value(t, typed=None) -> Optional[Value]:
    if typed is None:
        typed = resolve_value_type(t, num=True)
        if typed is None:
            return None
    return typed(t)


def is_structure(t: dict) -> bool:
    for key in t.keys():
        if type(key) != str:
            return False
    return True


def resolve_value_type(t, num=False) -> Optional[Type[Value]]:
    if isinstance(t, str):
        if len(t) == 1:
            return Char
        else:
            return String
    elif isinstance(t, float):
        return Float64
    elif isinstance(t, bool):
        return Boolean
    elif isinstance(t, int):
        if num is False:
            return NumericalValue
        else:
            return resolve_int_type(t)
    elif isinstance(t, bytes):
        return Bytes
    else:
        return None


def resolve_int_type(t: int) -> Type[Value]:
    if t >= 0:
        if t < 0xFF:
            return Unsigned8
        elif t < 0xFFFF:
            return Unsigned16
        elif t < 0xFFFFFFFF:
            return Unsigned32
        elif t < 0xFFFFFFFFFFFFFFFF:
            return Unsigned64
        else:
            return Unsigned128
    else:
        if t >= -0x8F:
            return Signed8
        elif t >= -0x8FFF:
            return Signed16
        elif t >= -0x8FFFFFFF:
            return Signed32
        elif t >= -0x8FFFFFFFFFFFFFFF:
            return Signed64
        else:
            return Unsigned128


def find_array_type(t) -> Optional[Type[Value]]:
    types = None
    for x in t:
        if types is None:
            types = resolve_value_type(x)
            if types is None:
                return None
        else:
            ts = resolve_value_type(x)
            if types != ts:
                if (issubclass(types, String) or issubclass(types, Char)) and (
                        issubclass(ts, String) or issubclass(ts, Char)):
                    types = String
                    continue
                else:
                    return None

    if issubclass(types, NumericalValue):
        a, b = min(t), max(t)
        if a < 0:
            if (a * -1) > b:
                return resolve_int_type(a)
            else:
                return resolve_int_type(-b)
        else:
            return resolve_int_type(b)
    else:
        return types
