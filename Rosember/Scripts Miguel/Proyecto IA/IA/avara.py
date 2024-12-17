from nodo import Nodo
from busqueda import Busqueda

class Avara(Busqueda):

  def __init__(self, entorno, inicio,punto_de_fuego_uno,punto_de_fuego_dos):
    lista_nodos = [Nodo(inicio[:], None, None, 0, entorno,punto_de_fuego_uno,punto_de_fuego_dos)]
    self.ruta2 = []
    super().__init__(lista_nodos)

    self.punto_inicio = inicio
    self.punto_de_fuego_uno = punto_de_fuego_uno
    self.punto_de_fuego_dos = punto_de_fuego_dos
  
  def heuristica(self,nodo_actual):
    valor_de_la_heuristica=0
    if nodo_actual.fuego_uno_apagado:
     valor_de_la_heuristica=abs(nodo_actual.estado[0]-self.punto_de_fuego_dos[0])+abs(nodo_actual.estado[1]-self.punto_de_fuego_dos[1])
     return valor_de_la_heuristica   
    elif nodo_actual.fuego_dos_apagado:
     valor_de_la_heuristica=abs(nodo_actual.estado[0]-self.punto_de_fuego_uno[0])+abs(nodo_actual.estado[1]-self.punto_de_fuego_uno[1])
     return valor_de_la_heuristica  
    else :
     valor_de_la_heuristica=abs(nodo_actual.estado[0]-self.punto_de_fuego_uno[0])+abs(nodo_actual.estado[1]-self.punto_de_fuego_uno[1])+abs(nodo_actual.estado[0]-self.punto_de_fuego_dos[0])+abs(nodo_actual.estado[1]-self.punto_de_fuego_dos[1])
     return valor_de_la_heuristica
    
  def busqueda(self):
    cantidad = 0
    nodo_actual = None


    while (len(self.lista_nodos) > 0):
        nodo_actual = self.lista_nodos.pop(0)
        nodo_padre = nodo_actual.padre

        if nodo_actual.es_meta():
            hoja = nodo_actual
            while hoja.padre is not None:
                self.ruta.append(hoja.estado)
                self.ruta2.append(hoja.costo)
                hoja = hoja.padre
            break
        
        elif nodo_actual.cubeta_en_mano == True and nodo_actual.cubeta_con_agua > 0:
           
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
                                  nodo_actual.fuego_apagado,
                                  nodo_actual.costo + self.heuristica(nodo_actual))

                self.actualizar_posicion(nodo_hijo, operador)
                #print(operador)
                #print(self.verificar_restricciones(nodo_hijo, nodo_padre, operador))
                if self.verificar_restricciones(nodo_hijo, nodo_padre, operador):
                    self.acciones_bombero(nodo_hijo)
                    self.lista_nodos.append(nodo_hijo)
                    lista_nodos = sorted(self.lista_nodos, key=lambda nodo: nodo.costo, reverse=True)



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
                                  nodo_actual.fuego_apagado,
                                  nodo_actual.costo + self.heuristica(nodo_actual))

                self.actualizar_posicion(nodo_hijo, operador)
                #print(operador)
                #print(self.verificar_restricciones(nodo_hijo, nodo_padre, operador))
                if self.verificar_restricciones(nodo_hijo, nodo_padre, operador) and self.evitar_ciclo(nodo_hijo, nodo_actual):
                    self.acciones_bombero(nodo_hijo)
                    self.lista_nodos.append(nodo_hijo)
                    lista_nodos = sorted(self.lista_nodos, key=lambda nodo: nodo.costo, reverse=True)

    self.actualizar_reporte(nodo_actual, cantidad)
    self.ruta.append(hoja.estado)
    self.ruta2.append(hoja.costo)
    self.ruta.reverse()
    self.ruta2.reverse()
    return self.ruta, self.ruta2