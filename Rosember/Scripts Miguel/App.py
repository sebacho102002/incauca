import tkinter as tk
from tkinter import messagebox
import subprocess
import threading

# Clase para mostrar tooltips al pasar el mouse
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="#ffffe0", relief="solid", borderwidth=1,
                         font=("tahoma", "10", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
        self.tipwindow = None

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Scripts para procesos AP")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        self.root.config(bg="#F4F6F8")

        self.frame_superior = tk.Frame(self.root, bd=2, relief="solid", bg="#005f73")
        self.frame_superior.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.titulo = tk.Label(self.frame_superior, text="Aplicación AP", font=("Helvetica", 18, "bold"), fg="white", bg="#005f73")
        self.titulo.pack(pady=10)

        self.frame_lateral = tk.Frame(self.root, bd=2, relief="solid", bg="#94d2bd")
        self.frame_lateral.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.frame_dinamico = tk.Frame(self.root, bd=2, relief="solid", bg="#e9d8a6")
        self.frame_dinamico.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.botones_laterales = {
            'Despoblación': ['Recibir_correos', 'Crear_poligonos', 'Enviar_correos_mapas', 'Enviar correos'],
            'Buscar': ['Annotations', '4'],
            'Abono': ['5', '6'],
            'D': ['7', '8']
        }

        # Diccionario de descripciones para los tooltips
        self.descripciones = {
            'Recibir_correos': "Recibe archivos Excel con información de suertes desde Outlook.",
            'Crear_poligonos': "Genera polígonos de cultivo a partir de los datos recibidos.",
            'Enviar_correos_mapas': "Envía los mapas de resiembra por correo electrónico.",
            'Enviar correos': "Envía correos de validación de zonas con adjuntos.",
            'Annotations': "Busca y verifica capas 'annotations' en manglar.",
            '4': "Script de búsqueda alternativo o adicional.",
            '5': "Proceso relacionado con fertilización o análisis de abono.",
            '6': "Módulo de control de abonos (detalles específicos en el script).",
            '7': "Utilidad experimental o en desarrollo.",
            '8': "Proceso auxiliar para tareas específicas de AP."
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
        threading.Thread(target=self._run_script_thread, args=(boton,)).start()

    def _run_script_thread(self, boton):
        try:
            result = subprocess.run(["python", f"C:/Geodata/Mapas_Despoblacion/Scripts Miguel/{boton}/main.py"],
                                    capture_output=True, text=True)
            if result.returncode == 0:
                self.show_message("Ejecución Exitosa", f"El script {boton} se ejecutó correctamente.")
            else:
                self.show_message("Error", f"Error al ejecutar main.py:\n\n{result.stderr}")
        except Exception as e:
            self.show_message("Error", f"Error al ejecutar main.py: {str(e)}")

    def mostrar_botones(self, boton):
        if self.botones[boton].cget('state') == 'disabled':
            return

        for widget in self.frame_dinamico.winfo_children():
            widget.destroy()

        titulo_metodo = tk.Label(self.frame_dinamico, text=f"Métodos {boton}", font=("Helvetica", 14, "bold"), fg="#005f73", bg="#e9d8a6")
        titulo_metodo.pack(pady=10)

        metodos = self.botones_laterales[boton]
        for metodo in metodos:
            label_metodo = tk.Label(self.frame_dinamico, text=f" {metodo}", font=("Arial", 12), bg="#e9d8a6")
            label_metodo.pack(pady=5)

            boton_metodo = tk.Button(self.frame_dinamico, text="Ejecutar", command=lambda m=metodo: self.run_script(m), height=2, width=15,
                                     bg="#008b8b", fg="white", font=("Helvetica", 12), relief="raised", bd=3, activebackground="#4CAF50")
            boton_metodo.pack(pady=10)

            # Tooltip para descripción
            descripcion = self.descripciones.get(metodo, "Sin descripción disponible.")
            Tooltip(boton_metodo, descripcion)

        for texto, boton_widget in self.botones.items():
            if texto == boton:
                boton_widget.config(state='disabled', bg='#006f6f')
            else:
                boton_widget.config(state='normal', bg="#008b8b")

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
