import tkinter as tk
from amplitud import Amplitud
from profundidad import Profundidad
from costo import Costo
from a_estrella import A_estrella
from avara import Avara

class Interfaz:
    def __init__(self, entorno, inicio,punto_de_fuego_uno,punto_de_fuego_dos):
        self.entorno = entorno
        self.ruta = []
        self.ruta2 = []
        self.index = 0
        self.inicio = inicio
        self.punto_de_fuego_uno=punto_de_fuego_uno
        self.punto_de_fuego_dos=punto_de_fuego_dos
        self.persona = None
        self.metodo = None
        self.mostrar_interfaz_grafica()

    def mostrar_interfaz_grafica(self):
        root = tk.Tk()
        root.title("Bombero inteligente")
        cell_size = 40
        canvas = tk.Canvas(root, width=len(self.entorno[0]) * cell_size, height=len(self.entorno) * cell_size)
        canvas.pack()
        # Crear función para dibujar el mapa

        def reiniciar():
            # Restablece el entorno y la posición inicial
            canvas.delete("all")
            draw_map()
            self.ruta = []
            self.ruta2 = []
            self.index = 0
            self.metodo = None
            x, y = self.inicio
            self.persona = canvas.create_oval(
                y * cell_size, x * cell_size,
                (y + 1) * cell_size, (x + 1) * cell_size, fill="yellow")
            estado_label.config(text="")

            costo_label.config(text="")
            ruta_label.config(text="")
            rendimiento_label.config(text="")

            amplitud_button.config(state="normal")
            costo_uniforme_button.config(state="normal")
            profundidad_button.config(state="normal")
            a_star_button.config(state="normal")
            avara_button.config(state="normal")

        def draw_map():
            for i in range(len(self.entorno)):
                for j in range(len(self.entorno[i])):
                    fill_color = ""
                    if self.entorno[i][j] == 0:
                        fill_color = "white"
                    elif self.entorno[i][j] == 1:
                        fill_color = "black"
                    elif self.entorno[i][j] == 2:
                        fill_color = "red"
                    elif self.entorno[i][j] == 3:
                        fill_color = "gray"
                    elif self.entorno[i][j] == 4:
                        fill_color = "gray"
                    elif self.entorno[i][j] == 6:
                        fill_color = "blue"
                    canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill=fill_color)

        draw_map()

        self.persona = canvas.create_oval(
            self.inicio[1] * cell_size, self.inicio[0] * cell_size,
            (self.inicio[1] + 1) * cell_size, (self.inicio[0] + 1) * cell_size, fill="yellow")

        def ejecutar_algoritmo():
            if self.metodo == "Amplitud":
                alg_busq = Amplitud(self.entorno, self.inicio)
                self.ruta = alg_busq.busqueda()
                mover_persona()
            elif self.metodo == "Profundidad":
                alg_busq = Profundidad(self.entorno, self.inicio)
                self.ruta = alg_busq.busqueda()
                mover_persona()
            elif self.metodo == "Costo":
                alg_busq = Costo(self.entorno, self.inicio)
                self.ruta, self.ruta2 = alg_busq.busqueda()
                mover_persona()
            elif self.metodo == "A*":
                alg_busq = A_estrella(self.entorno, self.inicio,self.punto_de_fuego_uno,self.punto_de_fuego_dos)
                self.ruta, self.ruta2 = alg_busq.busqueda()
                mover_persona()
            elif self.metodo == "Avara":
                alg_busq = Avara(self.entorno, self.inicio,self.punto_de_fuego_uno,self.punto_de_fuego_dos)
                self.ruta, self.ruta2 = alg_busq.busqueda()
                mover_persona()
            
            ruta_label.config(text=f"Ruta de Solución: {self.ruta}")
            rendimiento_label.config(text=f"Rendimiento: {alg_busq.reporte}")
            costo_label.config(text=f"Costo: {self.ruta2}")


        def mover_persona():
            if self.index < len(self.ruta):
                x, y = self.ruta[self.index]
                canvas.coords(self.persona, y * cell_size, x * cell_size, (y + 1) * cell_size, (x + 1) * cell_size)
                self.index += 1
                if self.index < len(self.ruta):
                    root.after(200, mover_persona)
                else:
                    estado_label.config(text="Finalizado: Meta Encontrada")
                    amplitud_button.config(state="disabled")
                    costo_uniforme_button.config(state="disabled")
                    profundidad_button.config(state="disabled")
                    a_star_button.config(state="disabled")
                    avara_button.config(state="disabled")

                    amplitud_button.config(bg="SystemButtonFace")
                    costo_uniforme_button.config(bg="SystemButtonFace")
                    profundidad_button.config(bg="SystemButtonFace")
                    a_star_button.config(bg="SystemButtonFace")
                    avara_button.config(bg="SystemButtonFace")
        
        def toggle_button(button):
            nonlocal amplitud_button, costo_uniforme_button, profundidad_button

            

            if button.cget("bg") == "gray":
                button.config(bg="SystemButtonFace")  # Cambia el color de fondo a predeterminado
                amplitud_button.config(state="normal")
                costo_uniforme_button.config(state="normal")
                profundidad_button.config(state="normal")
                a_star_button.config(state="normal")
                avara_button.config(state="normal")
            else:
                button.config(bg="gray")
                if self.metodo == "Amplitud":
                    costo_uniforme_button.config(state="disabled")
                    profundidad_button.config(state="disabled")
                    a_star_button.config(state="disabled")
                    avara_button.config(state="disabled")
                    

                elif self.metodo == "Profundidad":
                    amplitud_button.config(state="disabled")
                    costo_uniforme_button.config(state="disabled")
                    a_star_button.config(state="disabled")
                    avara_button.config(state="disabled")

                elif self.metodo == "Costo":
                    profundidad_button.config(state="disabled")
                    amplitud_button.config(state="disabled")
                    a_star_button.config(state="disabled")
                    avara_button.config(state="disabled")

                elif self.metodo == "A*":
                    profundidad_button.config(state="disabled")
                    amplitud_button.config(state="disabled")
                    costo_uniforme_button.config(state="disabled")
                    avara_button.config(state="disabled")

                elif self.metodo == "Avara":
                    profundidad_button.config(state="disabled")
                    amplitud_button.config(state="disabled")
                    a_star_button.config(state="disabled")
                    costo_uniforme_button.config(state="disabled")
                    

        # Botón de reinicio
        

        def set_nombre_metodo(nombre_metodo):
            self.metodo = nombre_metodo

        def actualizar_ruta_label():
            ruta_label.config(text=f"Ruta de Solución: {self.ruta}")

        def actualizar_ruta_label():
            ruta_label.config(text=f"Ruta de Solución: {self.ruta}")


        ruta_label = tk.Label(root, text="Ruta de Solución:")
        ruta_label.pack()

        costo_label = tk.Label(root, text="Costo:")
        costo_label.pack()

        rendimiento_label = tk.Label(root, text="Rendimiento:")
        rendimiento_label.pack()

        # Contenedor para botones informados
        frame_informados = tk.Frame(root)
        frame_informados.pack(pady=5)

        # Etiqueta de algoritmos informados
        label_informados = tk.Label(frame_informados, text="Busqueda Informada:")
        label_informados.pack(side="top")

        # Botón para A*
        a_star_button = tk.Button(frame_informados, text="A*", command=lambda: (set_nombre_metodo("A*"), toggle_button(a_star_button)), bg="SystemButtonface")
        a_star_button.pack(side="left", padx=20)

        # Botón para Avara
        avara_button = tk.Button(frame_informados, text="Avara", command=lambda: (set_nombre_metodo("Avara"), toggle_button(avara_button)), bg="SystemButtonface")
        avara_button.pack(side="left", padx=5)

        # Contenedor para botones no informados
        frame_no_informados = tk.Frame(root)
        frame_no_informados.pack(pady=10)

        # Etiqueta de algoritmos no informados
        label_no_informados = tk.Label(frame_no_informados, text="Busqueda no informada:")
        label_no_informados.pack(side="top", pady=5)

        # Botón para Amplitud
        amplitud_button = tk.Button(frame_no_informados, text="Amplitud", command=lambda: (set_nombre_metodo("Amplitud"), toggle_button(amplitud_button)), bg="SystemButtonface")
        amplitud_button.pack(side="left", padx=5)

        # Botón para Costo Uniforme
        costo_uniforme_button = tk.Button(frame_no_informados, text="Costo Uniforme", command=lambda: (set_nombre_metodo("Costo"), toggle_button(costo_uniforme_button)), bg="SystemButtonface")
        costo_uniforme_button.pack(side="left", padx=5)

        # Botón para Profundidad
        profundidad_button = tk.Button(frame_no_informados, text="Profundidad", command=lambda: (set_nombre_metodo("Profundidad"), toggle_button(profundidad_button)), bg="SystemButtonface")
        profundidad_button.pack(side="left", padx=5)

        button_frame = tk.Frame(root)
        button_frame.pack(side="bottom", pady=10)

        # Botón para Comenzar
        start_button = tk.Button(button_frame, text="Comenzar", command=lambda: ejecutar_algoritmo())
        start_button.pack(side="left")

        # Botón para Reiniciar
        reiniciar_button = tk.Button(button_frame, text="Reiniciar", command=reiniciar)
        reiniciar_button.pack(side="left")

        estado_label = tk.Label(root, text="")
        estado_label.pack()

        root.mainloop()