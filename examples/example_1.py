import tycho

data = {"foo": "Hello World", "bar": 10, "baz": True}
print(tycho.to_bytes(data).hex(" "))
# 40 03 03 66 6f 6f 1e 0b 48 65 6c 6c 6f 20 57 6f 72 6c 64 03 62 61 72 11 0a 03 62 61 7a 10 01
