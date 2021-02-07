import tycho

print(tycho.serialise({1: True, 2: False, 3: True, 4: False}))
print(tycho.serialise([1, 2, 3, 4]))
print(tycho.serialise([1, 2, 3, False]))