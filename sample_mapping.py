class A:
    def __init__(self, name) -> None:
        self.name = name
        print("A constructed")

class B:
    def __init__(self, name) -> None:
        self.name = name
        print("B constructed")

    def start(self):
        print("B called")

class C:
    def __init__(self, name) -> None:
        self.name = name
        print("C constructed")
    

def get_A(name):
    return A(name=name)

def get_B(name):
    return B(name=name)

def get_C(name):
    return C(name=name)

mp = {
    "brand name": {
        "model version 1": get_A,
        "model version 2" : get_B,
        "model version 3" : get_C,
    }
}

name = "Kimaya"
bname = "brand name"
mversion = "model version 2"

func = mp[bname][mversion]
objB = func(name=name)
objB.start()
