
class Nodo:
    
    def __init__(self, estado, padre, operador, profundidad, entorno,punto_de_fuego_uno,punto_de_fuego_dos ,cubeta_en_mano=False, cubeta_con_agua=0, capacidad_cubeta=0, fuego_apagado=0, costo=0,valor_heuristica=0,costo_mas_heuristica=0,fuego_uno_apagado=False,fuego_dos_apagado=False):
        self.estado = estado # [f, c] ubicación actual del bombero
        self.padre = padre   # Nodo
        self.operador = operador # izquierda, arriba, derecha o abajo
        self.profundidad = profundidad
        self.entorno = entorno # varible para los algoritmos que modifican el ambiente|1
        self.punto_de_fuego_uno=punto_de_fuego_uno
        self.punto_de_fuego_dos=punto_de_fuego_dos
        self.cubeta_en_mano = cubeta_en_mano # true o false
        self.cubeta_con_agua = cubeta_con_agua # 0, 1, 2
        self.capacidad_cubeta = capacidad_cubeta # 0, 1 o 2
        self.fuego_apagado = fuego_apagado # 0, 1 o 2
        self.fuego_uno_apagado = fuego_uno_apagado
        self.fuego_dos_apagado = fuego_dos_apagado

        self.costo = costo # variable para los algoritmos que requieren costo
        self.costo_mas_heuristica = costo_mas_heuristica
        self._valor_heuristica = valor_heuristica

    def es_meta(self):
        return self.fuego_apagado == 2
    
  
    def get_estado(self):
        return self.estado
    
    def get_padre(self):
        return self.padre
    
    def get_operador(self):
        return self.operador
    
    def get_profundidad(self):
        return self.profundidad
    
    def get_entorno(self):
        return self.entorno
    
    def get_cubeta_en_mano(self):
        return self.cubeta_en_mano
    
    def get_cubeta_con_agua(self):
        return self.cubeta_con_agua
    
    def get_capacidad_cubeta(self):
        return self.capacidad_cubeta
    
    def get_fuego_apagado(self):
        return self.fuego_apagado
    
    def get_costo(self):
        return self.costo
    
    def get_valor_heuristica(self):
     return self.get_valor_heuristica
    
    def get_costo_mas_heuristica(self):
     return self.get_costo_mas_heuristica
    
    def get_fuego_uno_apagado(self):
        return self.fuego_dos_apagado
    
    def get_fuego_dos_apagado(self):
        return self.fuego_dos_apagado

    def set_estado(self, estado):
        self.estado = estado

    def set_padre(self, padre):
        self.padre = padre

    def set_operador(self, operador):
        self.operador = operador

    def set_profundidad(self, profundidad):
        self.profundidad = profundidad

    def set_entorno(self, entorno):
        self.entorno = entorno

    def set_cubeta_en_mano(self, cubeta_en_mano):
        self.cubeta_en_mano = cubeta_en_mano

    def set_cubeta_con_agua(self, cubeta_con_agua):
        self.cubeta_con_agua = cubeta_con_agua

    def set_capacidad_cubeta(self, capacidad_cubeta):
        self.capacidad_cubeta = capacidad_cubeta

    def set_fuego_apagado(self, fuego_apagado):
        self.fuego_apagado = fuego_apagado

    def set_costo(self, costo):
        self.costo = costo
