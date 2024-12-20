import pandas as pd
import os
import win32com.client as win32
import tkinter as tk
from tkinter import filedialog, messagebox

def enviar_email(to_addrs, cc_addrs, subject, body, archivos):
    """Envía un correo electrónico con archivos adjuntos."""
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = to_addrs
    mail.CC = cc_addrs
    mail.Subject = subject
    mail.Body = body

    for archivo in archivos:
        mail.Attachments.Add(archivo)
    mail.Send()

def confirmar_envio():
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    return messagebox.askyesno("Confirmación", "Los archivos han sido creados. ¿Desea enviar los correos?")

def seleccionar_archivo():
    """Abre una ventana para seleccionar un archivo Excel con una ruta predeterminada."""
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    ruta_predeterminada = 'C:/Users/jsbejaranob/Desktop/prueba'
    archivo_seleccionado = filedialog.askopenfilename(
        initialdir=ruta_predeterminada,
        title="Seleccionar archivo Excel",
        filetypes=(("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*"))
    )
    if not archivo_seleccionado:
        raise FileNotFoundError("No se seleccionó ningún archivo. El proceso fue cancelado.")
    return archivo_seleccionado

def main():
    try:
        # Seleccionar el archivo Excel principal
        print("Seleccione el archivo Excel principal (Incauca.xlsx)...")
        file_path = seleccionar_archivo()

        # Ruta del archivo de correos
        correos_path = 'C:/Users/jsbejaranob/Desktop/prueba/Correos.xlsx'  # Este archivo debe estar fijo

        # Establecer la carpeta de salida como la misma que la de entrada
        output_folder = os.path.dirname(file_path)
        output_proveedores = os.path.join(output_folder, 'Proveedores')
        os.makedirs(output_proveedores, exist_ok=True)  # Crear carpeta si no existe

        # Cargar los archivos Excel
        print("Cargando archivos Excel...")
        df = pd.read_excel(file_path, sheet_name='Hoja1')
        correos_df = pd.read_excel(correos_path)

        # Convertir la columna de fecha (columna 'Ult.Cor/Siem') a formato corto
        print("Corrigiendo formato de fecha en la columna 'Ult.Cor/Siem'...")
        df['Ult.Cor/Siem'] = pd.to_datetime(df['Ult.Cor/Siem'], errors='coerce').dt.strftime('%d/%m/%Y')

        # Filtrar datos con "Tenencia" igual a 51 para generar el archivo "Proveedores"
        print("Filtrando datos de 'Tenencia' con valor 51...")
        df_proveedores = df[df['Tenencia'] == 51]

        # Guardar el archivo de proveedores consolidado
        proveedores_file = os.path.join(output_proveedores, 'Incauca_Proveedores.xlsx')
        df_proveedores.to_excel(proveedores_file, index=False, sheet_name='Proveedores')
        print(f'Archivo de proveedores generado: {proveedores_file}\n')

        # Eliminar los datos de proveedores del DataFrame original
        df = df[df['Tenencia'] != 51]

        # Filtrar el DataFrame por la columna "Zona"
        print("Filtrando datos por 'Zona'...")
        zonas_unicas = df['Zona'].unique()

        # Crear archivos por zona
        archivos_generados = []
        for zona in zonas_unicas:
            print(f"Generando archivo para la zona: {zona}...")
            df_filtrado = df[df['Zona'] == zona]
            output_file = os.path.join(output_folder, f'{zona.replace(" ", "_")}.xlsx')
            df_filtrado.to_excel(output_file, index=False, sheet_name=zona)
            print(f'Archivo generado: {output_file}')
            archivos_generados.append((zona, output_file))

        # Confirmar envio de correos
        if not confirmar_envio():
            print("Envío de correos cancelado.")
            return

        # Enviar correos por zona
        correos_por_zona = {
            'Oriental Incauca': ('jsbejarano2002@gmail.com', 'predeterminado@ejemplo.com'),
            'Central Incauca': ('jsbejarano2002@gmail.com', 'predeterminado@ejemplo.com'),
            'Sur Incauca': ('jsbejarano2002@gmail.com', 'predeterminado@ejemplo.com'),
            'Jamundí Incauca': ('jsbejarano2002@gmail.com', 'predeterminado@ejemplo.com'),
            'Occidental Incauca': ('jsbejarano2002@gmail.com', 'predeterminado@ejemplo.com'),
            'Norte Incauca': ('jsbejarano2002@gmail.com', 'predeterminado@ejemplo.com'),
            'Sur Occidental Incauca': ('jsbejarano2002@gmail.com', 'predeterminado@ejemplo.com')
        }

        for zona, output_file in archivos_generados:
            to_addrs, cc_addrs = correos_por_zona.get(zona, ('correo_predeterminado@ejemplo.com', 'copia_predeterminado@ejemplo.com'))
            subject = f'Datos de la Zona {zona}'
            body = f"Adjunto encontrará los datos correspondientes a la zona {zona}.\n\nEste es un mensaje automático generado por el sistema. Por favor, no responder."
            print(f"Enviando correo a {to_addrs} con copia a {cc_addrs}...")
            enviar_email(to_addrs, cc_addrs, subject, body, [output_file])
            print(f'Correo enviado a {to_addrs} con copia a {cc_addrs} con el archivo {output_file}\n')

        # Procesar proveedores para enviar correos individualmente
        print("Enviando correos a proveedores...")
        proveedores_unicos = df_proveedores['Nombre'].unique()
        for proveedor in proveedores_unicos:
            print(f"Procesando proveedor: {proveedor}...")
            df_proveedor = df_proveedores[df_proveedores['Nombre'] == proveedor]
            output_file = os.path.join(output_proveedores, f'Proveedores_{proveedor.replace(" ", "_")}.xlsx')
            df_proveedor.to_excel(output_file, index=False, sheet_name=proveedor)
            print(f'Archivo generado para proveedor {proveedor}: {output_file}')

            # Buscar correos en la tabla de correos
            correos = correos_df[correos_df['Proveedor'] == proveedor]
            if correos.empty:
                print(f"No se encontraron correos para el proveedor: {proveedor}")
                continue

            to_addrs = correos.iloc[0]['Correo Principal']
            cc_addrs = correos.iloc[0]['CC'] if pd.notna(correos.iloc[0]['CC']) else ''
            subject = f'Datos del Proveedor: {proveedor}'
            body = f"Adjunto encontrará los datos correspondientes al proveedor {proveedor}.\n\nEste es un mensaje automático generado por el sistema. Por favor, no responder."

            print(f"Enviando correo a {to_addrs} con copia a {cc_addrs}...")
            enviar_email(to_addrs, cc_addrs, subject, body, [output_file])
            print(f'Correo enviado a {to_addrs} con copia a {cc_addrs} con el archivo {output_file}\n')

        print("Proceso finalizado.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        input("Presione Enter para salir...")

if __name__ == "__main__":
    main()
