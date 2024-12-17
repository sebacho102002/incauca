from nodo import Nodo  # Importa la clase Nodo desde nodo

nodo_inicial = Nodo(matriz, None, None, 0)
cola_nodos = [nodo_inicial]


def leerMatriz(file_path):
    with open(file_path, 'r') as file:
        matriz = [linea.strip().split() for linea in file.readlines()]
    return matriz

matriz = leerMatriz("C:\\Users\\rodri\\Desktop\\IA\\Prueba1.txt")

def busqueda():
    while cola_nodos:
        nodo_actual = cola_nodos.pop(0)
        for direccion in ['arriba', 'abajo', 'izquierda', 'derecha']:
            hijo = mover(direccion)
            if hijo is not None:
                cola_nodos.append(hijo)

                
def encontrar_inicio(matriz):
    for fila_index, fila in enumerate(matriz):
        for col_index, valor in enumerate(fila):
            if valor == '5':
                return fila_index, col_index
    return None



def mover(direccion):
        # Copia la matriz actual para evitar modificar la original
        nueva_entorno = [fila[:] for fila in matriz]
        
        fila, columna = encontrar_inicio(nuevo_entorno)
        dx, dy = movimientos[direccion]
        nueva_fila = fila + dx
        nueva_columna = columna + dy
        capacidad_cubeta = 0
        cubeta_en_mano = false
        cubeta_con_agua = false
        
        # Definir movimientos posibles
        movimientos = {
            'arriba': (-1, 0),
            'abajo': (1, 0),
            'izquierda': (0, -1),
            'derecha': (0, 1)
        }
        
        if direccion in movimientos:  
            # Verificar si la nueva posición está dentro de los límites de la matriz
            if 0 <= nueva_fila < len(nueva_entorno) and 0 <= nueva_columna < len(nueva_entorno[0]):
                # Verificar si la nueva posición es una casilla libre (contiene '0')
                if nueva_entorno[nueva_fila][nueva_columna] == '0':
                    # Realizar el movimiento
                    nueva_entorno[fila][columna], nueva_entorno[nueva_fila][nueva_columna] = nueva_entorno[nueva_fila][nueva_columna], nueva_entorno[fila][columna]
                    return Nodo(nueva_entorno,cola_nodos[0], direccion, self.profundidad + 1)
                elif nueva_entorno[nueva_fila][nueva_columna] == '3':
                    cubeta = 1
                    
                    
        
        # Si la dirección no es válida o el movimiento no es posible, devolvemos None
        return None



        