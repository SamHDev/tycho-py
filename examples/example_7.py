data = bytes.fromhex("500b696e69742e7365727665724001036b6579400201657103010001016e714080e95b480b79c302b5c3bed04d57dd155f4efef3ebdc0e9abc533b1b2bc67f30c80407b12ed0f711f007becc54215b1526ec92406306218ef176132adf7df441e37af0c141e47229343f68dd8c89a4570442c833396b3f033a6d99179024a7061841171e3175e7864f019ebbbf6734adff3048f31a4098ba12ea0e15cd951c02af")

import tycho

print(tycho.from_bytes(data))