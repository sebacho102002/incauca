from nodo import Nodo
from busqueda import Busqueda

class Amplitud(Busqueda):

    def __init__(self, entorno, inicio):
        lista_nodos = [Nodo(inicio[:], None, None, 0, entorno,None,None)]
        super().__init__(lista_nodos)
    
        

    def busqueda(self):
        cantidad = 0
        nodo_actual = None
        

        while self.lista_nodos:
            nodo_actual = self.lista_nodos.pop(0)
            nodo_padre = nodo_actual.padre

            if nodo_actual.es_meta():
                hoja = nodo_actual
                while hoja.padre is not None:
                    self.ruta.append(hoja.estado)
                    hoja = hoja.padre
                break
            

            else:
                cantidad += 1
                for operador in self.operadores:
                    nodo_hijo = Nodo(nodo_actual.estado,
                                      nodo_actual,
                                      operador,
                                      nodo_actual.profundidad + 1,
                                      nodo_actual.entorno,
                                      nodo_actual.punto_de_fuego_uno,
                                      nodo_actual.punto_de_fuego_dos,
                                      nodo_actual.cubeta_en_mano,
                                      nodo_actual.cubeta_con_agua,
                                      nodo_actual.capacidad_cubeta,
                                      nodo_actual.fuego_apagado)
                    
                    self.actualizar_posicion(nodo_hijo, operador)
                    #print(operador)
                    #print(self.verificar_restricciones(nodo_hijo, nodo_padre, operador))
                    if self.verificar_restricciones(nodo_hijo, nodo_padre, operador):
                        self.acciones_bombero(nodo_hijo)
                        self.lista_nodos.append(nodo_hijo)
 
        self.actualizar_reporte(nodo_actual, cantidad)
        self.ruta.append(hoja.estado)
        self.ruta.reverse()
        
        return self.ruta