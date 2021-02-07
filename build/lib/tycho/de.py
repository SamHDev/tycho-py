from tycho.elements import *
from tycho.values import *
import typing


def deserialise(s: Element) -> typing.Any:
    if isinstance(s, Unit):
        return None
    elif isinstance(s, Value):
        return s.__getattribute__("value")
    elif isinstance(s, Option):
        if s.is_none:
            return None
        else:
            return deserialise(s)
    elif isinstance(s, Array):
        return [deserialise(e) for e in s.value]
    elif isinstance(s, Structure):
        return {str(k): deserialise(e) for k, e in s.value.items()}
    elif isinstance(s, Variant):
        return dict((s.name, deserialise(s.value)))
    elif isinstance(s, Map):
        return {deserialise_value(k): deserialise(e) for k, e in s.value.items()}
    elif isinstance(s, List):
        return {deserialise_value(k) for k, e in s.value}


def deserialise_value(s: Value):
    if isinstance(s, String) or isinstance(s, Char):
        return s.value
    elif isinstance(s, NumericalValue):
        return s.value
    elif isinstance(s, Boolean):
        return s.value
    elif isinstance(s, Bytes):
        return s.value
