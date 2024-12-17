from nodo import Nodo
from busqueda import Busqueda


class Profundidad(Busqueda):
    def __init__(self, entorno, inicio):
        super().__init__([Nodo(inicio, None, None, 0, entorno,None,None)])
        
    
    def busqueda(self):
        cantidad = 0
        nodo_actual = None
        pila_nodos = self.lista_nodos
        
        while pila_nodos:
            #print(len(pila_nodos))
            nodo_actual = pila_nodos.pop()
            nodo_padre = nodo_actual.padre
            profundidad_actual = nodo_actual.profundidad
            
           
            if nodo_actual.es_meta():
                hoja = nodo_actual
                #print(len(pila_nodos))
                while hoja.padre is not None:
                    self.ruta.append(hoja.estado)
                    hoja = hoja.padre
                break
            else:
                cantidad += 1
                for operador in self.operadores.__reversed__():
                    nodo_hijo = Nodo(
                        nodo_actual.estado,
                        nodo_actual,
                        operador,
                        profundidad_actual + 1,
                        nodo_actual.entorno,
                        nodo_actual.punto_de_fuego_uno,
                        nodo_actual.punto_de_fuego_dos,
                        nodo_actual.cubeta_en_mano,
                        nodo_actual.cubeta_con_agua,
                        nodo_actual.capacidad_cubeta,
                        nodo_actual.fuego_apagado
                    )
                    self.actualizar_posicion(nodo_hijo, operador)
                    
                    
                    if self.verificar_restricciones(nodo_hijo, nodo_padre, operador) and self.evitar_ciclo(nodo_hijo, nodo_actual):
                       self.acciones_bombero(nodo_hijo)
                       pila_nodos.append(nodo_hijo)
                    


                   

        self.actualizar_reporte(nodo_actual, cantidad)
        self.ruta.append(hoja.estado)
        self.ruta.reverse()
        return self.ruta