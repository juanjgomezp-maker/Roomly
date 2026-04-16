from Habitacion import Habitacion

class Familiar(Habitacion):
    def __init__(self, numero, piso):
        super().__init__(numero, piso, "familiar", 150, 4)