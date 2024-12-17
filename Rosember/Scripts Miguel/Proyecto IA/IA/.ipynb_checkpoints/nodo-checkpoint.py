 class Nodo:
    
    
    def __init__(self, entorno, padre, operador, profundidad):
        self.entorno = entorno
        self.padre = padre
        self.operador = operador
        self.profundidad = 0
        
    # Métodos getters
    def get_entorno(self):
        return self.entorno

    def get_padre(self):
        return self.padre

    def get_operador(self):
        return self.operador

    def get_profundidad(self):
        return self.profundidad
    
    
        
    #print(entorno)
    #print(profundidad)
        
