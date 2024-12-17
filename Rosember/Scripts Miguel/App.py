import tkinter as tk
from tkinter import messagebox
import subprocess
import threading


class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Scripts para procesos AP")
        
        # Configurar el tamaño fijo de la ventana
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Frame superior para el título
        self.frame_superior = tk.Frame(self.root, bd=2, relief="solid")
        self.frame_superior.pack(side=tk.TOP, fill=tk.X, pady=5)
        
        self.titulo = tk.Label(self.frame_superior, text="Aplicación AP", font=("Helvetica", 16))
        self.titulo.pack(pady=10)
        
        # Frame para los botones laterales
        self.frame_lateral = tk.Frame(self.root, bd=2, relief="solid")
        self.frame_lateral.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Frame para los botones dinámicos
        self.frame_dinamico = tk.Frame(self.root, bd=2, relief="solid")
        self.frame_dinamico.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Botones laterales
        self.botones_laterales = {
            'Despoblación': ['Recibir_correos', 'Crear_poligonos', 'Enviar_correos_mapas'],
            'B': ['3', '4'],
            'C': ['5', '6'],
            'D': ['7', '8'],
            'Mapas':['Ordenar archivos', 'Enviar correos']
        }
        
        self.botones = {}
        for texto in self.botones_laterales.keys():
            boton = tk.Button(self.frame_lateral, text=texto, command=lambda btnl=texto: self.mostrar_botones(btnl), height=2, width=10)
            boton.pack(fill=tk.X, pady=5)
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
            self.show_message("Error", f"Error al ejecutar main.py")

    
    def mostrar_botones(self, boton):
        # Si el botón presionado ya está habilitado, simplemente retornamos
        if self.botones[boton].cget('state') == 'disabled':
            return
        
        # Eliminar todos los widgets en el frame_dinamico
        for widget in self.frame_dinamico.winfo_children():
            widget.destroy()
        
        # Crear título según el botón lateral presionado
        titulo_metodo = tk.Label(self.frame_dinamico, text=f"Métodos {boton}", font=("Helvetica", 14))
        titulo_metodo.pack(pady=10)
        
        # Crear botones según el botón lateral presionado
        metodos = self.botones_laterales[boton]
        for metodo in metodos:
            label_metodo = tk.Label(self.frame_dinamico, text=f" {metodo}", font=("Arial", 10))
            label_metodo.pack(pady=5)
            boton_metodo = tk.Button(self.frame_dinamico, text="Ejecutar", command=lambda m=metodo: self.run_script(m), height=2, width=10)
            boton_metodo.pack(pady=5)
        
        # Habilitar el botón presionado y deshabilitar los otros
        for texto, boton_widget in self.botones.items():
            if texto == boton:
                boton_widget.config(state='disabled', bg='gray')  # Cambiar color a gris
            else:
                boton_widget.config(state='normal', bg='SystemButtonFace')  # Restaurar color normal


if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
