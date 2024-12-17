from datetime import datetime
  # Importa la clase Nodo desde nodo


class Busqueda:

    def __init__(self, lista_nodos):
        self.lista_nodos = lista_nodos
        self.ruta = []
        self.reporte = {
            'nodos_expandidos': 0,
            'profundidad_arbol': 0,
            'tiempo_computo': '0:00:00.0'
        }
        self.tiempo_inicio = datetime.now()
        self.operadores = ['izquierda', 'arriba','derecha', 'abajo',]
    
    def busqueda():
        pass # metodo abstracto que se implementa en las clases hijas


    
        # metodo que actualiza la posicion en el nodo hijo segun la direccion
    def actualizar_posicion(self, nodo_hijo, operador):
        f, c = nodo_hijo.estado


        if operador == 'arriba':
            nodo_hijo.estado = (f - 1, c)
        elif operador == 'abajo':
            nodo_hijo.estado = (f + 1, c)
        elif operador == 'izquierda':
            nodo_hijo.estado = (f, c - 1)
        elif operador == 'derecha':
            nodo_hijo.estado = (f, c + 1)

       
    # metodo para actualizar valores dek reporte
    def actualizar_reporte(self, nodo_hijo, cantidad):
        tiempo_actual = datetime.now()

        # Calcular el tiempo de cómputo como la diferencia entre la hora actual y la hora de inicio
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio
        tiempo_computo = str(tiempo_transcurrido)

        # Actualizar el reporte con la cantidad de nodos expandidos, profundidad y tiempo de cómputo
        self.reporte['nodos_expandidos'] = cantidad
        self.reporte['profundidad_arbol'] = nodo_hijo.profundidad
        self.reporte['tiempo_computo'] = tiempo_computo


    # Metodo que valida si la posicion en la que se mueve el hijo tiene alguna restriccio(muro, fuera de los limites, fuego sin agua) o no
    def verificar_restricciones(self, nodo_hijo, nodo_padre, operador):
        f, c = nodo_hijo.estado
        entorno = nodo_hijo.entorno

        # Verificar si el movimiento es válido en términos de límites del entorno
        if (operador == 'arriba' and f >= 0) or \
            (operador == 'abajo' and f < len(entorno)) or \
            (operador == 'izquierda' and c >= 0) or \
            (operador == 'derecha' and c < len(entorno[0])):
                

                if entorno[f][c] == 1:
                    return False

                elif entorno[f][c] == 2 and nodo_hijo.cubeta_con_agua == 0:
                    return False
                
                elif nodo_padre is None:
                    return True
            
                elif nodo_padre is not None:

                    if (nodo_padre.estado, nodo_padre.cubeta_con_agua, nodo_padre.capacidad_cubeta, nodo_padre.cubeta_en_mano) ==\
                          (nodo_hijo.estado, nodo_hijo.cubeta_con_agua, nodo_hijo.capacidad_cubeta, nodo_hijo.cubeta_en_mano):
                        
                        return False
                    
                    else:
                        return True
                else:
                    return True
                    
        else:
                return False


    # metodo que si el movimento es correcto del bombero, ver que accion tomar
    def acciones_bombero(self, nodo_hijo):
        entorno = nodo_hijo.entorno[:]
        f, c = nodo_hijo.estado

        if (entorno[f][c] == 3 or entorno[f][c] == 4) and nodo_hijo.cubeta_en_mano == False:
            ent_temp = entorno[f][:]
            if entorno[f][c] == 3:
                ent_temp[c] = 0
                entorno[f] = ent_temp
                nodo_hijo.entorno = entorno
                nodo_hijo.cubeta_en_mano = True
                nodo_hijo.capacidad_cubeta = 1
            else:
                ent_temp[c] = 0
                entorno[f] = ent_temp
                nodo_hijo.entorno = entorno
                nodo_hijo.cubeta_en_mano = True
                nodo_hijo.capacidad_cubeta = 2

        elif entorno[f][c] == 6 and nodo_hijo.cubeta_con_agua == 0:
            # Llenar la cubeta con agua 
            if nodo_hijo.cubeta_en_mano:
               if nodo_hijo.capacidad_cubeta == 1:
                nodo_hijo.cubeta_con_agua = 1
               elif nodo_hijo.capacidad_cubeta == 2:
                nodo_hijo.cubeta_con_agua = 2
            
        elif entorno[f][c] == 2 and nodo_hijo.cubeta_con_agua > 0:
        # Apagar el fuego (reemplazar la casilla por 0)
            ent_temp = entorno[f][:]
            ent_temp[c] = 0
            entorno[f] = ent_temp
            nodo_hijo.entorno = entorno
            nodo_hijo.fuego_apagado += 1
            nodo_hijo.cubeta_con_agua -= 1

            if nodo_hijo.punto_de_fuego_uno == nodo_hijo.estado:
                nodo_hijo.fuego_uno_apagado=True
            elif nodo_hijo.punto_de_fuego_dos == nodo_hijo.estado:
                nodo_hijo.fuego_dos_apagado=True



    def evitar_ciclo(self, nodo_hijo, nodo_padre):

        if (nodo_hijo.cubeta_en_mano == True):
            estados_visitados = []
            nodo = nodo_padre
            while nodo.cubeta_en_mano ==True:
             estados_visitados.append(nodo.estado)
             nodo = nodo.padre
            
            if (nodo_hijo.fuego_apagado == 1):
                estados_visitados = []
                nodo = nodo_padre
                while nodo.fuego_apagado == 1:
                 estados_visitados.append(nodo.estado)
                 nodo = nodo.padre
                if nodo_hijo.estado not in estados_visitados:
                 return True
                else:
                 return False
                
            elif nodo_hijo.estado not in estados_visitados:
             return True
            else:
             return False
        
        else:
            estados_visitados = []
            nodo = nodo_padre
            while nodo.padre is not None:
             estados_visitados.append(nodo.estado)
             nodo = nodo.padre
            estados_visitados.append(nodo.estado)
            if nodo_hijo.estado not in estados_visitados:
             return True
            else:
             return False


    
    




    
