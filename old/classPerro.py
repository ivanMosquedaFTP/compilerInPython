# Definir la clase
class Perro:
    # Constructor: se ejecuta cuando creamos un nuevo objeto
    def __init__(self, nombre, raza, edad):
        self.nombre = nombre  # Atributo del objeto
        self.raza = raza
        self.edad = edad

    # Método para que el perro ladre
    def ladrar(self):
        print(f"{self.nombre} dice: ¡Guau, guau!")

    # Método para mostrar información del perro
    def info(self):
        return f"Nombre: {self.nombre}, Raza: {self.raza}, Edad: {self.edad} años"
    
    


# Crear objetos (instancias de la clase Perro)
perro1 = Perro("Fido", "Labrador", 3)
perro2 = Perro("Max", "Pastor Alemán", 5)

# Usar los métodos de los objetos
perro1.ladrar()  # Fido dice: ¡Guau, guau!
print(perro1.info())  # Nombre: Fido, Raza: Labrador, Edad: 3 años

perro2.ladrar()  # Max dice: ¡Guau, guau!
print(perro2.info())  # Nombre: Max, Raza: Pastor Alemán, Edad: 5 años




