from .elements import Unit, Option, Array, Structure, Variant, Map, List, Element
from .values import Boolean, Unsigned8, Unsigned16, Unsigned32, Unsigned64, Unsigned128, Signed8, Signed16, Signed32, \
    Signed64, Signed128, Char, String, Bytes, Value

from . import length
from . import ser as __ser__
from . import de as __de__
from .decode import decode as __decode__


def encode(s: Element) -> bytes:
    """
    Encode an Element object into tycho bytes.
    :param s:
    :return:
    """
    return s.encode()


def decode(s: bytes) -> Element:
    """
    Decode tycho bytes into Element object(s)
    :param s:
    :return:
    """
    return __decode__(s)


def serialise(s: dict or list or bool or int or float or str or bytes or None) -> Element:
    """
    Serialise a python object into a Element object(s)
    :param s:
    :return:
    """
    return __ser__.serialise(s)


def deserialise(s: Element) -> dict or list or bool or int or float or str or bytes or None:
    """
    Deserialise a Element object into python object(s)
    :param s:
    :return:
    """
    return __de__.deserialise(s)


def to_bytes(s: dict or list or bool or int or float or str or bytes or None) -> bytes:
    """
    Encode a python object into tycho bytes.

    Same as: `encode(serialise(object))`
    :param s:
    :return:
    """
    return encode(serialise(s))


def from_bytes(s: bytes) -> dict or list or bool or int or float or str or bytes or None:
    """
    Decode tycho bytes into a python object.

    Same as: `deserialise(decode(object))`
    :param s:
    :return:
    """
    return deserialise(decode(s))


__tycho__ = "0.4.0"
