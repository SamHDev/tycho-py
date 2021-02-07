# Tycho Python

A python implementation of the [tycho binary format](https://github.com/samhdev/tycho).

### Features
- Full Implementation
- Serialise/Deserialise python objects into binary format.
- Uses Builtin errors/types.
- No dependencies


### Installation
You can install using pip:
```
pip install tycho-py
```

or add the following to your requirements file:
```
tycho-py==0.1.0
```

Once installed, import the library:
```python
import tycho
```

## Documentation

### Basic usage
The following example takes a python object and encodes it into tycho bytes.
```python
import tycho
data = {"foo": "Hello World", "bar": 10, "baz": True}
tycho.to_bytes(data).hex(" ")
# 40 03 03 66 6f 6f 1e 0b 48 65 6c 6c 6f 20 57 6f 72 6c 64 03 62 61 72 11 0a 03 62 61 7a 10 01
```

The following example takes a tycho bytes and decodes it into bytes.
```python
import tycho

data = bytes.fromhex("40 03 03 66 6f 6f 1e 0b 48 65 6c 6c 6f 20 57 6f 72 6c 64 03 62 61 72 11 0a 03 62 61 7a 10 01")
print(tycho.from_bytes(data))  
# {'foo': 'Hello World', 'bar': 10, 'baz': True}
```

### Advanced usage
As python does not map to the rust/serde data model, types have to be inferred. 
When encoding from a python object into bytes two processes take place, Serialisation and Encoding.
See this diagram below.
```
Python Object
   \/    /\      Serialise
Tycho Classes
   \/    /\      Encoding
    Bytes          
```

Serialisation is expensive, as types have to matched and inferred. 
To allow better quicker encoding, the `Tycho Classes` are exposed to the user.

These reproduce the same result as above examples.
```python
import tycho

data = tycho.Structure({
    "foo": tycho.String("Hello World"),
    "bar": tycho.Unsigned8(10),
    "baz": tycho.Boolean(False)
})
print(tycho.encode(data))
# 40 03 03 66 6f 6f 1e 0b 48 65 6c 6c 6f 20 57 6f 72 6c 64 03 62 61 72 11 0a 03 62 61 7a 10 01
```

```python
import tycho

data = bytes.fromhex("40 03 03 66 6f 6f 1e 0b 48 65 6c 6c 6f 20 57 6f 72 6c 64 03 62 61 72 11 0a 03 62 61 7a 10 01")
print(tycho.decode(data))
# Structure({'foo': String('Hello World'), 'bar': Unsigned8(10), 'baz': Boolean(True)})
```

Using the `Tycho Classes` also allow for usage of the `Variant` Object. As python does not have rust-like enums,
there is no serialisation/deserialisation implemented for them.

Within the library these `Tycho Classes` are named `Elements` to keep parity between the rust library and others.

### Methods
- `tycho.encode(element) -> bytes`
    - Encode an Element object into bytes
    
- `tycho.decode(bytes) -> Element`
    - Decode bytes into an Element
    
- `tycho.serialise(object) -> Element` 
    - Serialise a python object into an element
    
- `tycho.deserialise(element) -> object` 
    - Deserialise a element into a python object
    
- `tycho.from_bytes(object) -> Element` 
    - Serialise and encode a python object into bytes.
    
- `tycho.deserialise(element) -> object` 
    - Decode and Deserialise bytes into a python object.

### Classes
#### Base classes
- `tycho.Element`
- `tycho.Value`
- `tycho.NumericalValue`

#### Type classes
- `tycho.Unit`
- `tycho.Option`
- `tycho.Structure`
- `tycho.Array`
- `tycho.Variant`
- `tycho.List`
- `tycho.Map`
- `tycho.Boolean`
- `tycho.Unsigned8`
- `tycho.Unsigned16`
- `tycho.Unsigned32`
- `tycho.Unsigned64`
- `tycho.Unsigned128`
- `tycho.Signed8`
- `tycho.Signed16`
- `tycho.Signed32`
- `tycho.Signed64`
- `tycho.Signed128`
- `tycho.Float32`
- `tycho.Float64`
- `tycho.Char`
- `tycho.String`
- `tycho.Bytes`


> ##### Warning
> Within the spec it is possible for a `Map` to contain `float32` and `float64`,
> However some libraries map not accept such values (due to their unhashability)
