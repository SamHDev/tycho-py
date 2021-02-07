import tycho
import debug

def gamer(name, title, score, admin):
    return tycho.Structure({
        "name": tycho.String(name),
        "title": tycho.String(title),
        "score": tycho.Unsigned16(score),
        "admin": tycho.Boolean(admin)
    })


data = tycho.Structure({
    "gamers": tycho.Array([
        gamer("Sam", "Real Developer", 100, True),
        gamer("James", "Fake Developer", 5, False)
    ]),
    "tags": tycho.List(tycho.String, [tycho.String("gamer"), tycho.String("developer"), tycho.String("score"), tycho.String("test")])
})

print(debug.print_element(0, data))

print(data.encode().hex(" "))