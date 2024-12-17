class Nodo:
    
    def __init__(self, estado, padre, operador, profundidad, entorno, cubeta_en_mano=False, cubeta_con_agua=0, capacidad_cubeta=0, fuego_apagado=0, costo=-1):
        self.estado = estado # [f, c] ubicación actual del bombero
        self.padre = padre   # Nodo
        self.operador = operador # izquierda, arriba, derecha o abajo
        self.profundidad = profundidad
        self.entorno = entorno # varible para los algoritmos que modifican el ambiente
        self.cubeta_en_mano = cubeta_en_mano # true o false
        self.cubeta_con_agua = cubeta_con_agua # 0, 1, 2
        self.capacidad_cubeta = capacidad_cubeta # 0, 1 o 2
        self.fuego_apagado = fuego_apagado # 0, 1 o 2
        self.costo = costo # variable para los algoritmos que requieren costo

    def es_meta(self):
        return self.fuego_apagado == 2
    
class Busqueda:

    def __init__(self, lista_nodos):
        self.lista_nodos = lista_nodos
        self.ruta = []
        self.reporte = {
            'nodos_expandidos': 0,
            'profundidad_arbol': 0,
            'tiempo_computo': '0:00:00.0'
        }
    
    def busqueda():
        pass # metodo abstracto que se implementa en las clases hijas

    def actualizar_posicion(self, nodo_actual, operador):
        f, c = nodo_actual.estado

        if operador == 'arriba':
            nodo_actual.estado = (f - 1, c)
        elif operador == 'abajo':
            nodo_actual.estado = (f + 1, c)
        elif operador == 'izquierda':
            nodo_actual.estado = (f, c - 1)
        elif operador == 'derecha':
            nodo_actual.estado = (f, c + 1)

       

    def actualizar_reporte(self, nodo_actual, cantidad):
        pass # añadir codigo para generar el reporte

    def verificar_restricciones(self, nodo_actual, nodo_padre, operador):
        f, c = nodo_actual.estado
        entorno = nodo_actual.entorno

        # Verificar si el movimiento es válido en términos de límites del entorno
        if operador == 'arriba' and f > 0:
            nuevo_estado = (f - 1, c)
        elif operador == 'abajo' and f < len(entorno) - 1:
            nuevo_estado = (f + 1, c)
        elif operador == 'izquierda' and c > 0:
            nuevo_estado = (f, c - 1)
        elif operador == 'derecha' and c < len(entorno[0]) - 1:
            nuevo_estado = (f, c + 1)
        else:
            return False
        
        if entorno[nuevo_estado[0]][nuevo_estado[1]] == 1:
        # No se puede mover a una casilla de obstáculo
            return False

        elif entorno[nuevo_estado[0]][nuevo_estado[1]] == 2 and nodo_actual.cubeta_con_agua == 0:
            return False
        
        elif (entorno[nuevo_estado[0]][nuevo_estado[1]] == 3 or entorno[nuevo_estado[0]][nuevo_estado[1]] == 4) and nodo_actual.capacidad_cubeta  > 0:
            return False
        
        return True
        

    def acciones_bombero(self, nodo_actual):
        entorno = nodo_actual.entorno
        f, c = nodo_actual.estado

        if (entorno[f][c] == 3 or entorno[f][c] == 4) and nodo_actual.cubeta_en_mano == False:

            ent_temp = entorno[f][:]
            if entorno[f][c] == 3:
                ent_temp[c] = 0
                nodo_actual.entorno[f] = ent_temp
                nodo_actual.cubeta_en_mano = True
                nodo_actual.capacidad_cubeta = 1
            else:
                ent_temp[c] = 0
                nodo_actual.entorno[f] = ent_temp
                nodo_actual.cubeta_en_mano = True
                nodo_actual.capacidad_cubeta = 2

        elif entorno[f][c] == 6:
            # Llenar la cubeta con agua 
            if nodo_actual.cubeta_en_mano:
               ent_temp = entorno[f][:]
               if nodo_actual.capacidad_cubeta == 1:
                nodo_actual.cubeta_con_agua = 1
               elif nodo_actual.cubeta_cubeta == 2:
                nodo_actual.cubeta_con_agua = 2
            
        elif entorno[f][c] == 2:
        # Apagar el fuego (reemplazar la casilla por 0)
            ent_temp = entorno[f][:]
            ent_temp[c] = 0
            nodo_actual.entorno[f] = ent_temp
            nodo_actual.fuego_apagado += 1


    # get y set

class Amplitud(Busqueda):

    def __init__(self, entorno, inicio):
        lista_nodos = [Nodo(inicio[:], None, None, 0, entorno)]
        super().__init__(lista_nodos)
    
    def busqueda(self):
        cantidad = 0
        nodo_actual = None

        while (len(self.lista_nodos) == 0):
            nodo_actual = self.lista_nodos.pop(0)

            if nodo_actual.es_meta():
                hoja = nodo_actual
                while hoja.padre is not None
                    ruta.insert(0, hoja.operador)
                    hoja = hoja.padre
                break
            else:
                nodo_padre = nodo_actual.padre
                cantidad += 1

                operadores = ['arriba', 'abajo', 'izquierda', 'derecha']

                for operador in operadores:
                    if self.verificar_restricciones(nodo_actual,nodo_padre,operador):
                        self.actualizar_posicion(nodo_actual, operador)
                        nuevo_entorno = [fila[:] for fila in nodo_actual.entorno]
                        nuevo_nodo = Nodo(nuevo_estado, nodo_actual, operador, nodo_actual.profundidad + 1, nuevo_entorno)


                # añadir codigo para obtener todos los nodos hijos del nodo actual
                # tener en cuenta todas las restricciones en cuanto a los limites del entorno, muros, 
                # del algoritmo y del proyecto (agua, hidratante, fuego, cubeta y movimiento)
                # para añadir el nodo hijo a la lista de nodos 
        
        self.actualizar_reporte(nodo_actual, cantidad)
        return self.ruta





class Main:

    def __init__(self):
        self.entorno = None
        self.inicio = None
        self.cargar_mapa()
        self.iniciar_programa()

    def cargar_mapa(self):
        self.entorno = [] # mapa 
        self.inicio = [] # coordenadas donde inicia el bombero 

    def iniciar_programa(self):
        alg_busq = Amplitud(self.entorno, self.inicio)
        ruta = alg_busq.busqueda()
        print(ruta)
        print(alg_busq.reporte)