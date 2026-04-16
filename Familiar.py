from Habitacion import Habitacion

class Doble(Habitacion):
    def __init__(self, numero, piso):
        super().__init__(numero, piso, "doble", 100, 2)
