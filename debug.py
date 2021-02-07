import tycho
import sys


def print_byte(indent, byte: bytes or int, label):
    if isinstance(byte, int):
        byte = bytes([byte])

    for i in range(0, len(byte)):
        if i == 0:
            print_indent(indent, hex(byte[i])[2:].rjust(2, "0") + " - " + label)
        else:
            print_indent(indent, hex(byte[i])[2:].rjust(2, "0") + "")


def print_indent(indent, text):
    print((indent * "\t") + text)


def print_string(indent, value, length_text, offset=1):
    string_data = value.encode("utf-8")

    print_byte(indent, tycho.length.encode_length(len(string_data)), f"{length_text} {len(string_data)}")
    for char in value:
        print_byte(indent + offset, char.encode("utf-8"), f"\"{char}\"")


def print_element(indent, element, prefix=True):
    if isinstance(element, tycho.String):
        if prefix:
            print_indent(indent, f"String(\"{element.value}\")")
        else:
            print_indent(indent, f"\"{element.value}\"")

    elif isinstance(element, tycho.Char):
        if prefix:
            print_indent(indent, f"Char(\'{element.value}\')")
        else:
            print_indent(indent, f"\"{element.value}\"")

    elif isinstance(element, tycho.Bytes):
        if prefix:
            print_indent(indent, f"Bytes(\'{element.value.hex()}\')")
        else:
            print_indent(indent, f"\"{element.value.hex()}\"")

    elif isinstance(element, tycho.Boolean):
        if prefix:
            if element.value:
                print_indent(indent, f"Boolean(true)")
            else:
                print_indent(indent, f"Boolean(false)")
        else:
            if element.value:
                print_indent(indent, f"true")
            else:
                print_indent(indent, f"false")

    elif isinstance(element, tycho.values.NumericalValue):
        if prefix:
            print_indent(indent, f"{str(element.__class__.__name__)}({element.value})")
        else:
            print_indent(indent, f"{element.value}")

    elif isinstance(element, tycho.elements.Unit):
        print_indent(indent, f"Unit")

    elif isinstance(element, tycho.elements.Option):
        if prefix:
            if element.value is None:
                print_byte(indent, 0x20, "Option::None")
            else:
                print_byte(indent, 0x21, "Option::Some")
        print_element(indent + 1, element.value)

    elif isinstance(element, tycho.elements.Array):
        if prefix:
            print_indent(indent, f"Array({len(element.value)})")
        i = 0
        for item in element.value:
            i += 1
            print_indent(indent + 1, f"[{i - 1}] ")
            print_element(indent + 2, item)

    elif isinstance(element, tycho.elements.Structure):
        if prefix:
            print_indent(indent, f"Structure({len(element.value)})")
        i = 0
        for key, item in element.value.items():
            i += 1
            print_indent(indent + 1, f"[{i - 1}] \"{key}\"")
            print_element(indent + 2, item)

    elif isinstance(element, tycho.elements.Variant):
        if prefix:
            print_byte(indent, 0x50, "Variant")
        print_string(indent + 1, element.name, "Variant name has length")
        print_element(indent + 1, element.value)

    elif isinstance(element, tycho.elements.Map):
        if prefix:
            print_byte(indent, 0x60 + element.key_type(1).encode_prefix(), "Map::" + element.key_type.__name__)

        i = 0
        for key, value in element.value.items():
            i += 1
            print_indent(indent + 1, f"(Element {i - 1})")
            print_element(indent + 1, key, prefix=False)
            print_element(indent + 2, value)

    elif isinstance(element, tycho.elements.List):
        if prefix:
            print_byte(indent, 0x70 + element.item_type(1).encode_prefix(), "List::" + element.item_type.__name__)

        i = 0
        for item in element.value:
            i += 1
            print_indent(indent + 1, f"(Element {i - 1})")
            print_element(indent + 1, item, prefix=False)


if __name__ == "__main__":
    data = " ".join(sys.argv[1:]).strip()

    if len(data) == 0:
        print("No input given, please specify bytes to debug")
        sys.exit(1)

    try:
        data = bytes.fromhex(data)
    except:
        print("Failed to parse hex into bytes")
        sys.exit(2)

    data_bytes = data
    data = tycho.decode(data)

    print_element(0, data)