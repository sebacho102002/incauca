from amplitud import Amplitud
from profundidad import Profundidad
from interfaz import Interfaz

class Main:

    def __init__(self):
        self.entorno = None
        self.inicio = None
        self.punto_de_fuego_uno = None
        self.punto_de_fuego_dos = None
        self.cargar_mapa()
        self.iniciar_programa()

    def cargar_mapa(self):
        try:
            with open("C:\Geodata\Mapas_Despoblacion\Scripts Miguel\Proyecto IA\IA/Prueba1.txt", 'r') as archivo_mapa:
                lineas = archivo_mapa.readlines()

                self.entorno = []

                for linea in lineas:
                    fila = []
                    for caracter in linea.strip():
                        if caracter.isdigit():  # Solo convertir caracteres numéricos
                            fila.append(int(caracter))
                    self.entorno.append(fila)

               
                for i, fila in enumerate(self.entorno):
                    for j, elemento in enumerate(fila):
                        if elemento == 5:
                            self.inicio = (i, j)

                for i, fila in enumerate(self.entorno):
                    for j, elemento in enumerate(fila):
                        if elemento == 2:
                            self.punto_de_fuego_uno = (i, j)
                        if self.punto_de_fuego_uno != None:
                         break
                    if self.punto_de_fuego_uno != None:
                        break

                for i, fila in enumerate(self.entorno):
                    for j, elemento in enumerate(fila):
                        if elemento == 2:
                            self.punto_de_fuego_dos = (i, j)
                        if self.punto_de_fuego_dos != None and self.punto_de_fuego_dos != self.punto_de_fuego_uno:
                         break
                    if self.punto_de_fuego_dos != None and self.punto_de_fuego_dos != self.punto_de_fuego_uno:
                        break
                            
        except FileNotFoundError:
            print("El archivo no se encontró.")

    
    def iniciar_programa(self):
        interfaz = Interfaz(self.entorno,self.inicio,self.punto_de_fuego_uno,self.punto_de_fuego_dos)
        

mi_programa = Main()