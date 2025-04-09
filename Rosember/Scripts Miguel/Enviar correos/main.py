import pandas as pd
import os
import win32com.client as win32
import tkinter as tk
from tkinter import filedialog, messagebox
import datetime

def enviar_email(to_addrs, cc_addrs, subject, body, archivos):
    """Envía un correo electrónico con archivos adjuntos."""
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = to_addrs  # Puede contener múltiples correos separados por ";"
    mail.CC = cc_addrs  # Puede contener múltiples correos separados por ";"
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
    ruta_predeterminada = 'C:\\Geodata\\Mapas_Despoblacion\\Envio Programa vuelo'
    archivo_seleccionado = filedialog.askopenfilename(
        initialdir=ruta_predeterminada,
        title="Seleccionar archivo Excel",
        filetypes=(("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*"))
    )
    if not archivo_seleccionado:
        messagebox.showerror("Error", "No se seleccionó ningún archivo. El proceso fue cancelado.")
        raise FileNotFoundError("No se seleccionó ningún archivo. El proceso fue cancelado.")
    return archivo_seleccionado

def notificar_haciendas_faltantes(haciendas_faltantes):
    """Muestra una ventana con las haciendas que no se encontraron en el archivo de correos."""
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Haciendas Faltantes", f"Las siguientes haciendas no tienen un proveedor asignado:\n{', '.join(haciendas_faltantes)}")

def mostrar_error(mensaje):
    """Muestra un mensaje de error en una ventana emergente."""
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", mensaje)

def mostrar_exito(mensaje):
    """Muestra un mensaje de éxito en una ventana emergente."""
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Proceso Completado", mensaje)

def main():
    try:
        # Seleccionar el archivo Excel principal
        file_path = seleccionar_archivo()

        # Ruta del archivo de correos
        correos_path = 'C:\\Geodata\\Mapas_Despoblacion\\Envio Programa vuelo\\Correos.xlsx'

        # Establecer la carpeta de salida como la misma que la de entrada
        output_folder = os.path.dirname(file_path)
        output_proveedores = os.path.join(output_folder, 'Proveedores')
        os.makedirs(output_proveedores, exist_ok=True)

        # Cargar los archivos Excel
        df = pd.read_excel(file_path, sheet_name='Hoja1')
        correos_df = pd.read_excel(correos_path)

        # Convertir la columna de fecha (columna 'Ult.Cor/Siem') a formato corto en español
        df['Ult.Cor/Siem'] = pd.to_datetime(df['Ult.Cor/Siem'], errors='coerce').dt.strftime('%d/%m/%Y')

        # Filtrar datos con "Tenencia" igual a 51 para generar el archivo "Proveedores"
        df_proveedores = df[df['Tenencia'] == 51]

        # Guardar el archivo de proveedores consolidado
        proveedores_file = os.path.join(output_proveedores, 'Incauca_Proveedores.xlsx')
        df_proveedores.to_excel(proveedores_file, index=False, sheet_name='Proveedores')

        # Eliminar los datos de proveedores del DataFrame original
        df = df[df['Tenencia'] != 51]

        # Filtrar el DataFrame por la columna "Zona"
        zonas_unicas = df['Zona'].unique()

        # Crear archivos por zona
        archivos_generados = []
        for zona in zonas_unicas:
            df_filtrado = df[df['Zona'] == zona]
            output_file = os.path.join(output_folder, f'{zona.replace(" ", "_")}.xlsx')
            df_filtrado.to_excel(output_file, index=False, sheet_name=zona)
            archivos_generados.append((zona, output_file))

        # Confirmar envio de correos
        if not confirmar_envio():
            mostrar_error("El proceso fue cancelado por el usuario.")
            return

        # Obtener el mes actual para incluirlo en el asunto
        mes_actual = datetime.datetime.now().strftime("%B")

        # Diccionario de correos por zona actualizado
        correos_por_zona = {
            'Oriental Incauca': ('efcastillo@incauca.com', 'dfcollazos@incauca.com', 'japenao@incauca.com'),
            'Central Incauca': ('nsinisterra@incauca.com', 'semora@incauca.com', 'japenao@incauca.com'),
            'Sur Incauca': ('hsaavedra@incauca.com', 'mizquierdo@incauca.com', 'japenao@incauca.com'),
            'Jamundí Incauca': ('h.zambrano31@gmail.com', 'jamarin@incauca.com', 'japenao@incauca.com'),
            'Occidental Incauca': ('jamorenol@incauca.com', 'arpuente@incauca.com', 'japenao@incauca.com'),
            'Norte Incauca': ('fcarbonero@incauca.com', 'lfgomez@incauca.com', 'japenao@incauca.com'),
            'Sur Occidental Incauca': ('lsaavedra@incauca.com', 'ammartinez@incauca.com', 'japenao@incauca.com')
        }

        # Enviar correos por zona
        for zona, output_file in archivos_generados:
            to_addrs_primary, to_addrs_optional, cc_addrs = correos_por_zona.get(
                zona, 
                ('correo_predeterminado@ejemplo.com', '', 'copia_predeterminado@ejemplo.com')
            )
            # Combinar correos de envío (separados por ";")
            to_addrs = to_addrs_primary
            if to_addrs_optional:
                to_addrs += f";{to_addrs_optional}"
            
            subject = f'Fotografía Aérea Drone 2025 {zona} - {mes_actual}'
            body = f"""Saludos,

Envío el listado de suertes para tomar fotografías aéreas con Drone la siguiente semana y determinar el mapa de resiembra, revisar las edades que se propone y señalar su aprobación.

Por favor indicarnos cuales son las suertes que se posponen una semana por bajo desarrollo (las plantas pequeñas no se detectan en la fotografía) o por alta maleza en el surco.

También señalar las suertes que no se realizan por los siguientes motivos: se resembraron o se resembrará en menos de una semana, programadas para renovación o la hacienda ya no pertenece al ingenio.

Los mapas de despoblación de las suertes aprobadas llegarán de 3 a 5 días después de la toma de fotografías, por favor esperar para realizar la labor de resiembra.

Gracias por la atención. Cordialmente Rosemberg Moreno  - Agricultura de precisión Incauca."""

            enviar_email(to_addrs, cc_addrs, subject, body, [output_file])

        # Procesar proveedores para enviar correos individualmente
        haciendas_faltantes = []
        proveedores_unicos = correos_df['Proveedor'].unique()
        for proveedor in proveedores_unicos:
            correos_proveedor = correos_df[correos_df['Proveedor'] == proveedor]
            haciendas_proveedor = correos_proveedor['Hacienda'].values
            df_proveedor_filtrado = df_proveedores[df_proveedores['Hacienda'].isin(haciendas_proveedor)]

            if df_proveedor_filtrado.empty:
                haciendas_faltantes.extend(haciendas_proveedor)
                continue

            to_addrs = correos_proveedor.iloc[0]['Correo Principal']
            cc_addrs = ';'.join(correos_proveedor.iloc[0]['CC'].split(';')) if pd.notna(correos_proveedor.iloc[0]['CC']) else ''
            output_file = os.path.join(output_proveedores, f'Proveedores_{proveedor.replace(" ", "_")}.xlsx')
            df_proveedor_filtrado.to_excel(output_file, index=False, sheet_name=proveedor)

            subject = f'Fotografía Aérea Drone 2025 {proveedor} - {mes_actual}'
            body = f"""Buena tarde, comparto consolidado de suertes para volar con drone para despoblación del mes {mes_actual}. GRACIAS

En Incauca estamos optimizando las labores de campo y cosecha mediante el uso de fotografías aéreas con Drone de alto detalle para determinar lo siguiente (ver documento pdf adjunto):
1.            Mapa despoblación y resiembra (Distribución de paquetes)
2.            Verificar área neta en caña. 
3.            Líneas de surco para cosechar con piloto automático y disminuir pisoteo de la maquinaria.
4.            Topografía para identificar problemas de drenaje. 
5.            Mapa de malezas.
Los mapas de resiembra de las suertes aprobadas llegaran de 3 a 5 días después de la toma de fotografías. Toda esta información se mostrará en la plataforma web https://gis.manglar.com/
El costo por hectárea de esta tecnología es de $ 30.500 acordada con la empresa CNX - Manglar, Incauca asumirá el 50% resultando un costo por hectárea para el proveedor de $ 15.250."""

            enviar_email(to_addrs, cc_addrs, subject, body, [output_file])

        if haciendas_faltantes:
            notificar_haciendas_faltantes(haciendas_faltantes)

        mostrar_exito("Todos los correos se enviaron exitosamente.")
    except Exception as e:
        mostrar_error(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()
