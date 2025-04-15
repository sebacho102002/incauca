import time
import pandas as pd
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- INTERFAZ INICIAL PARA SELECCIÓN DE ARCHIVOS ---
root = tk.Tk()
root.withdraw()

input_file = filedialog.askopenfilename(
    title="Selecciona el archivo Excel de entrada",
    filetypes=[("Archivos de Excel", "*.xlsx")]
)
if not input_file:
    messagebox.showerror("Error", "No se seleccionó ningún archivo de entrada.")
    exit()

output_file = filedialog.asksaveasfilename(
    defaultextension=".xlsx",
    filetypes=[("Archivo Excel", "*.xlsx")],
    title="Selecciona la ubicación para guardar el archivo de salida"
)
if not output_file:
    messagebox.showerror("Error", "No se seleccionó archivo de salida.")
    exit()

# --- CONFIGURAR VENTANA DE PROGRESO ---
progress_win = tk.Tk()
progress_win.title("Procesando códigos en Manglar")
progress_label = tk.Label(progress_win, text="Iniciando proceso...")
progress_label.pack(padx=20, pady=(20, 10))
progress_bar = Progressbar(progress_win, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(padx=20, pady=(0, 20))
progress_win.update()

# --- VENTANA FINAL DE APAGADO CON CANCELAR ---
def mostrar_ventana_apagado():
    countdown_win = tk.Tk()
    countdown_win.title("⚠ Apagado programado")

    label = tk.Label(countdown_win, text="El equipo se apagará en 10 segundos.\nHaz clic en 'Cancelar' para evitarlo.")
    label.pack(padx=20, pady=(20, 10))

    cancel_button = tk.Button(countdown_win, text="Cancelar apagado", command=lambda: cancelar_apagado(countdown_win))
    cancel_button.pack(pady=(0, 20))

    def countdown():
        for i in range(10, 0, -1):
            label.config(text=f"El equipo se apagará en {i} segundos.\nHaz clic en 'Cancelar' para evitarlo.")
            countdown_win.update()
            time.sleep(1)
        countdown_win.destroy()
        os.system("shutdown /s /t 1")

    threading.Thread(target=countdown).start()
    countdown_win.mainloop()

def cancelar_apagado(win):
    win.destroy()
    messagebox.showinfo("Cancelado", "El apagado fue cancelado correctamente.")

# --- FUNCIÓN PRINCIPAL DEL SCRIPT ---
def ejecutar_script():
    try:
        # Configurar Selenium
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        wait = WebDriverWait(driver, 20)
        results = []

        # Ingresar a Manglar
        driver.get("https://gis.manglar.com/")
        wait.until(EC.presence_of_element_located((By.NAME, "inputEmail")))

        # Login
        driver.find_element(By.NAME, "inputEmail").send_keys("romorenoo@incauca.com")
        driver.find_element(By.NAME, "inputPassword").send_keys("EmmanuelR5034*")
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        wait.until(EC.url_contains("/dashboard"))

        # Leer archivo de entrada
        df = pd.read_excel(input_file, usecols=["Field"])
        total = len(df)
        progress_bar["maximum"] = total

        # Ir a mapas
        driver.get("https://gis.manglar.com/maps")
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search Fields']")))

        for index, row in df.iterrows():
            field_code = str(row["Field"]).strip()
            progress_label.config(text=f"Buscando: {field_code} ({index+1}/{total})")
            progress_bar["value"] = index + 1
            progress_win.update()

            try:
                search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search Fields']")))
                search_box.send_keys(Keys.CONTROL + "a")
                search_box.send_keys(Keys.BACKSPACE)
                time.sleep(1)

                for char in field_code:
                    search_box.send_keys(char)
                    time.sleep(0.1)

                time.sleep(0.5)
                search_box.send_keys(Keys.BACKSPACE)
                time.sleep(0.3)
                search_box.send_keys(field_code[-1])
                time.sleep(0.5)

                search_box.send_keys(Keys.RETURN)
                time.sleep(6)

                try:
                    annotation_label = driver.find_element(By.XPATH, "//span[contains(text(), 'Annotations')]")
                    try:
                        date_element = annotation_label.find_element(By.XPATH, "./preceding-sibling::span[contains(@class, 'badge')]")
                        annotation_date = date_element.text.strip()
                    except:
                        annotation_date = "No encontrada"
                    results.append((field_code, annotation_date))
                except:
                    results.append((field_code, "No"))

            except Exception as e:
                print(f"❌ Error con {field_code}: {e}")
                results.append((field_code, "Error"))

        # Guardar archivo de salida
        pd.DataFrame(results, columns=["Field", "Fecha_Annotations"]).to_excel(output_file, index=False)

    except Exception as e:
        messagebox.showerror("Error inesperado", f"Se ha producido un error:\n{e}")

    finally:
        try:
            driver.quit()
        except:
            pass
        try:
            if progress_win.winfo_exists():
                progress_win.destroy()
        except:
            pass
        mostrar_ventana_apagado()

# --- EJECUTAR EN HILO PARA NO BLOQUEAR LA VENTANA ---
threading.Thread(target=ejecutar_script).start()
progress_win.mainloop()
