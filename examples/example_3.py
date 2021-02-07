import tycho

data = tycho.Structure({
    "foo": tycho.String("Hello World"),
    "bar": tycho.Unsigned8(10),
    "baz": tycho.Boolean(False)
})
print(tycho.encode(data))