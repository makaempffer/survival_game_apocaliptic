class Persona:
    def __init__(self, nombre, edad, altura):
        self.nombre = nombre
        self.edad = edad
        self.altura = altura
    
    def print_nombre(self):
        print(self.nombre)


vale = Persona("valetina", 21, 1.20)
vale.print_nombre()
