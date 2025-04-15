import tkinter as tk
from tkinter import messagebox
import subprocess
import threading

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Scripts para procesos AP")
        
        # Configurar el tamaño fijo de la ventana
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # Configurar color de fondo de la ventana principal
        self.root.config(bg="#F4F6F8")
        
        # Frame superior para el título
        self.frame_superior = tk.Frame(self.root, bd=2, relief="solid", bg="#005f73")
        self.frame_superior.pack(side=tk.TOP, fill=tk.X, pady=10)
        
        self.titulo = tk.Label(self.frame_superior, text="Aplicación AP", font=("Helvetica", 18, "bold"), fg="white", bg="#005f73")
        self.titulo.pack(pady=10)
        
        # Frame para los botones laterales
        self.frame_lateral = tk.Frame(self.root, bd=2, relief="solid", bg="#94d2bd")
        self.frame_lateral.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Frame para los botones dinámicos
        self.frame_dinamico = tk.Frame(self.root, bd=2, relief="solid", bg="#e9d8a6")
        self.frame_dinamico.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botones laterales con colores mejorados
        self.botones_laterales = {
            'Despoblación': ['Recibir_correos', 'Crear_poligonos', 'Enviar_correos_mapas', 'Enviar correos'],
            'Buscar': ['Annotations', '4'],
            'Abono': ['5', '6'],
            'D': ['7', '8']
        }
        
        self.botones = {}
        for texto in self.botones_laterales.keys():
            boton = tk.Button(self.frame_lateral, text=texto, command=lambda btnl=texto: self.mostrar_botones(btnl), height=2, width=15,
                              bg="#008b8b", fg="white", font=("Helvetica", 12), relief="raised", bd=3, activebackground="#4CAF50")
            boton.pack(fill=tk.X, pady=8, padx=5)
            self.botones[texto] = boton

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def run_script(self, boton):
        # Ejecutar el script en un hilo separado
        threading.Thread(target=self._run_script_thread, args=(boton,)).start()
        
    def _run_script_thread(self, boton):
        try:
            # Ejecutar el script main.py
            result = subprocess.run(["python", f"C:/Geodata/Mapas_Despoblacion/Scripts Miguel/{boton}/main.py"], capture_output=True, text=True)
            if result.returncode == 0:
                self.show_message("Ejecución Exitosa", f"El script {boton} se ejecutó correctamente.")
            else:
                self.show_message("Error", f"Error al ejecutar main.py:\n\n{result.stderr}")
        except Exception as e:
            self.show_message("Error", f"Error al ejecutar main.py: {str(e)}")

    def mostrar_botones(self, boton):
        # Si el botón presionado ya está habilitado, simplemente retornamos
        if self.botones[boton].cget('state') == 'disabled':
            return
        
        # Eliminar todos los widgets en el frame_dinamico
        for widget in self.frame_dinamico.winfo_children():
            widget.destroy()
        
        # Crear título según el botón lateral presionado
        titulo_metodo = tk.Label(self.frame_dinamico, text=f"Métodos {boton}", font=("Helvetica", 14, "bold"), fg="#005f73", bg="#e9d8a6")
        titulo_metodo.pack(pady=10)
        
        # Crear botones según el botón lateral presionado
        metodos = self.botones_laterales[boton]
        for metodo in metodos:
            label_metodo = tk.Label(self.frame_dinamico, text=f" {metodo}", font=("Arial", 12), bg="#e9d8a6")
            label_metodo.pack(pady=5)
            boton_metodo = tk.Button(self.frame_dinamico, text="Ejecutar", command=lambda m=metodo: self.run_script(m), height=2, width=15,
                                     bg="#008b8b", fg="white", font=("Helvetica", 12), relief="raised", bd=3, activebackground="#4CAF50")
            boton_metodo.pack(pady=10)
        
        # Habilitar el botón presionado y deshabilitar los otros
        for texto, boton_widget in self.botones.items():
            if texto == boton:
                boton_widget.config(state='disabled', bg='#006f6f')  # Cambiar color a gris
            else:
                boton_widget.config(state='normal', bg="#008b8b")  # Restaurar color normal


if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
