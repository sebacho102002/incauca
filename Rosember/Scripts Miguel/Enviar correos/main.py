import pandas as pd
import os
import win32com.client as win32
import tkinter as tk
from tkinter import filedialog, messagebox
import datetime
import locale
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# Establecer la localización a español para que los meses salgan en español
try:
    locale.setlocale(locale.LC_TIME, 'es_ES')
except:
    locale.setlocale(locale.LC_TIME, 'es_CO.utf8')

def enviar_email(to_addrs, cc_addrs, subject, body, archivos):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = to_addrs
    mail.CC = cc_addrs
    mail.Subject = subject
    mail.Body = body
    for archivo in archivos:
        mail.Attachments.Add(archivo)
    mail.Send()

def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    ruta_predeterminada = 'C:\\Geodata\\Mapas_Despoblacion\\Envio Programa vuelo'
    archivo = filedialog.askopenfilename(
        initialdir=ruta_predeterminada,
        title="Seleccionar archivo Excel",
        filetypes=(("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*"))
    )
    if not archivo:
        messagebox.showerror("Error", "No se seleccionó ningún archivo.")
        raise FileNotFoundError("No se seleccionó ningún archivo.")
    return archivo

def mostrar_confirmacion():
    root = tk.Tk()
    root.withdraw()
    return messagebox.askyesno("Confirmación", "¿Desea enviar los correos generados?")

def mostrar_mensaje(titulo, mensaje):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(titulo, mensaje)

def mostrar_error(mensaje):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", mensaje)

def copiar_formato_y_datos(df, archivo_base, hoja_salida, archivo_salida):
    wb_base = load_workbook(archivo_base)
    ws_base = wb_base.active

    wb_nuevo = load_workbook(archivo_base)
    wb_nuevo.remove(wb_nuevo.active)
    ws_nuevo = wb_nuevo.create_sheet(hoja_salida)

    # Copiar formato
    for row in ws_base.iter_rows():
        for cell in row:
            new_cell = ws_nuevo.cell(row=cell.row, column=cell.col_idx, value=cell.value)
            if cell.has_style:
                new_cell._style = cell._style

    # Sobrescribir con datos del DataFrame
    for i, fila in enumerate(dataframe_to_rows(df, index=False, header=True), start=1):
        for j, valor in enumerate(fila, start=1):
            ws_nuevo.cell(row=i, column=j, value=valor)

    # Ajustar anchos de columna A y C
    ws_nuevo.column_dimensions['A'].width = 25
    ws_nuevo.column_dimensions['C'].width = 35
    ws_nuevo.column_dimensions['J'].width = 25

    wb_nuevo.save(archivo_salida)

def main():
    try:
        archivo_datos = seleccionar_archivo()
        archivo_correos = 'C:\\Geodata\\Mapas_Despoblacion\\Envio Programa vuelo\\Correos.xlsx'
        carpeta_salida = os.path.dirname(archivo_datos)
        carpeta_proveedores = os.path.join(carpeta_salida, 'Proveedores')
        os.makedirs(carpeta_proveedores, exist_ok=True)

        df = pd.read_excel(archivo_datos, sheet_name='Hoja1')
        correos_df = pd.read_excel(archivo_correos)

        df['Ult.Cor/Siem'] = pd.to_datetime(df['Ult.Cor/Siem'], errors='coerce').dt.strftime('%d/%m/%Y')

        df_proveedores = df[df['Tenencia'] == 51]
        df = df[df['Tenencia'] != 51]

        archivo_prov = os.path.join(carpeta_proveedores, 'Incauca_Proveedores.xlsx')
        copiar_formato_y_datos(df_proveedores, archivo_datos, 'Proveedores', archivo_prov)

        archivos_zonas = []
        for zona in df['Zona'].unique():
            df_zona = df[df['Zona'] == zona]
            archivo_zona = os.path.join(carpeta_salida, f'{zona.replace(" ", "_")}.xlsx')
            copiar_formato_y_datos(df_zona, archivo_datos, zona, archivo_zona)
            archivos_zonas.append((zona, archivo_zona))

        if not mostrar_confirmacion():
            mostrar_error("El proceso fue cancelado.")
            return

        mes_actual = datetime.datetime.now().strftime('%B')

        correos_por_zona = {
            'Oriental Incauca': ('efcastillo@incauca.com', 'dfcollazos@incauca.com', 'japenao@incauca.com'),
            'Central Incauca': ('nsinisterra@incauca.com', 'semora@incauca.com', 'japenao@incauca.com'),
            'Sur Incauca': ('hsaavedra@incauca.com', 'mizquierdo@incauca.com', 'japenao@incauca.com'),
            'Jamundí Incauca': ('h.zambrano31@gmail.com', 'jamarin@incauca.com', 'japenao@incauca.com'),
            'Occidental Incauca': ('jamorenol@incauca.com', 'arpuente@incauca.com', 'japenao@incauca.com'),
            'Norte Incauca': ('fcarbonero@incauca.com', 'lfgomez@incauca.com', 'japenao@incauca.com'),
            'Sur Occidental Incauca': ('lsaavedra@incauca.com', 'ammartinez@incauca.com', 'japenao@incauca.com')
        }

        for zona, archivo_zona in archivos_zonas:
            to, opcional, cc = correos_por_zona.get(zona, ('default@correo.com', '', 'defaultcc@correo.com'))
            destinatarios = f"{to};{opcional}" if opcional else to

            asunto = f'Fotografía Aérea Drone 2025 {zona} - {mes_actual.capitalize()}'
            cuerpo = f"""Saludos,

Envío el listado de suertes para tomar fotografías aéreas con Drone la siguiente semana y determinar el mapa de resiembra, revisar las edades que se propone y señalar su aprobación.

Por favor indicarnos cuales son las suertes que se posponen una semana por bajo desarrollo (las plantas pequeñas no se detectan en la fotografía) o por alta maleza en el surco.

También señalar las suertes que no se realizan por los siguientes motivos: se resembraron o se resembrará en menos de una semana, programadas para renovación o la hacienda ya no pertenece al ingenio.

Los mapas de despoblación de las suertes aprobadas llegarán de 3 a 5 días después de la toma de fotografías, por favor esperar para realizar la labor de resiembra.

Gracias por la atención. Cordialmente Rosemberg Moreno - Agricultura de precisión Incauca."""

            enviar_email(destinatarios, cc, asunto, cuerpo, [archivo_zona])

        haciendas_faltantes = []
        for proveedor in correos_df['Proveedor'].unique():
            correos_proveedor = correos_df[correos_df['Proveedor'] == proveedor]
            haciendas = correos_proveedor['Hacienda'].values
            df_prov = df_proveedores[df_proveedores['Hacienda'].isin(haciendas)]

            if df_prov.empty:
                haciendas_faltantes.extend(haciendas)   
                continue

            to = correos_proveedor.iloc[0]['Correo Principal']
            cc = correos_proveedor.iloc[0]['CC'] if pd.notna(correos_proveedor.iloc[0]['CC']) else ''
            archivo = os.path.join(carpeta_proveedores, f'Proveedores_{proveedor.replace(" ", "_")}.xlsx')
            copiar_formato_y_datos(df_prov, archivo_datos, proveedor, archivo)

            asunto = f'Fotografía Aérea Drone 2025 {proveedor} - {mes_actual.capitalize()}'
            cuerpo = f"""Buena tarde, comparto consolidado de suertes para volar con drone para despoblación del mes {mes_actual.capitalize()}. GRACIAS

En Incauca estamos optimizando las labores de campo y cosecha mediante el uso de fotografías aéreas con Drone de alto detalle para determinar lo siguiente:
1. Mapa despoblación y resiembra (Distribución de paquetes)
2. Verificar área neta en caña. 
3. Líneas de surco para cosechar con piloto automático y disminuir pisoteo de la maquinaria.
4. Topografía para identificar problemas de drenaje. 
5. Mapa de malezas.

Los mapas de resiembra de las suertes aprobadas llegaran de 3 a 5 días después de la toma de fotografías. Toda esta información se mostrará en la plataforma web https://gis.manglar.com/

El costo por hectárea de esta tecnología es de $30.500 acordada con la empresa CNX - Manglar, Incauca asumirá el 50% resultando un costo por hectárea para el proveedor de $15.250."""

            enviar_email(to, cc, asunto, cuerpo, [archivo])

        if haciendas_faltantes:
            mostrar_mensaje("Haciendas Faltantes", f"No se encontraron estas haciendas en el archivo de proveedores:\n{', '.join(haciendas_faltantes)}")

        mostrar_mensaje("Éxito", "Todos los correos fueron enviados correctamente.")

    except Exception as e:
        mostrar_error(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()
