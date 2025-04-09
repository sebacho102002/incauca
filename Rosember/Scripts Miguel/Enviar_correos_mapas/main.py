import os
import pandas as pd
import win32com.client as win32
import datetime

# Ruta del archivo Excel
excel_path = r'C:\Geodata\Mapas_Despoblacion\Scripts Miguel\Enviar_correos_mapas\correos.xlsx'
# Ruta de la carpeta principal
base_folder = r'C:\Geodata\Mapas_Despoblacion\Envio mapas zonas'
# Número de la semana actual
current_week = datetime.datetime.now().isocalendar()[1]

folder_name = f"Zonas 2025{current_week:02d}"

# Leer las hojas en el archivo Excel
xls = pd.ExcelFile(excel_path)
if 'Propias' not in xls.sheet_names and 'Proveedores' not in xls.sheet_names:
    raise ValueError("Worksheet named 'correo' not found")

# Leer el archivo Excel
df_propias = pd.read_excel(excel_path, sheet_name='Propias')
df_proveedores = pd.read_excel(excel_path, sheet_name='Proveedores', dtype={'COD HDA': str})

#print("Columnas en el DataFrame:", df_propias.columns)
#print("Datos en el DataFrame:", df_proveedores)


def enviar_email(to_addrs, cc_addrs, subject, body, Archivos):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = '; '.join(to_addrs)
    mail.CC = '; '.join(cc_addrs)
    mail.Subject = subject
    mail.Body = body

    for attachment_path in Archivos:
        mail.Attachments.Add(attachment_path)
    mail.Send()


def propias():

    for index, row in df_propias.iterrows():
        zona = row['ZONA'].strip()
        to_addrs = row['CORREO PARA'].split(';')
        cc_addrs = row['CON COPIA A:'].split(';')
        subject = row['ASUNTO']
        body = row['CUERPO MENSAJE']

        zone_folder = os.path.join(base_folder, folder_name, zona)
        print(zone_folder)
        
        if not os.path.exists(zone_folder):
            print(f"Carpeta no encontrada para la zona: {zona}")
            continue
        Archivos_pdf_propias = [os.path.join(zone_folder, f) for f in os.listdir(zone_folder) if f.endswith('.pdf')]

        if not Archivos_pdf_propias:
            print(f"No se encontraron archivos PDF para la zona: {zona}")
            continue
        enviar_email(to_addrs, cc_addrs, subject, body, Archivos_pdf_propias)
        print(f"Correo enviado para la zona: {zona}")

def proveedores():
    archivos_prov = os.path.join(base_folder, folder_name, "Proveedores")

    if not os.path.exists(archivos_prov):#verifica que exista archivo
        print(f"Carpeta no encontrada para la zona: Proveedores")
        return

    archivos_pdf_proveedores = [os.path.join(archivos_prov, f) for f in os.listdir(archivos_prov) if f.endswith('.pdf')]# Lista todos los archivos PDF en la carpeta de proveedores
    archivos_por_hda = {}
    
    for archivo in archivos_pdf_proveedores:
        nombre_archivo = os.path.basename(archivo)
        partes = nombre_archivo.split('_') 
        hda = partes[2]
        if hda not in archivos_por_hda:
            archivos_por_hda[hda] = []  
        archivos_por_hda[hda].append(archivo)  

    # Verifica si no se encontraron archivos PDF
    if not archivos_por_hda:
        return
    grupo_correo = df_proveedores.groupby('CORREO PARA')

    for email, group in grupo_correo: # Recorre cada grupo de correos electrónicos y toma datos
        to_addrs = email.split(';') 
        cc_addrs = group['CON COPIA A:'].iloc[0].split(';')
        subject = group['ASUNTO'].iloc[0]
        body = group['CUERPO MENSAJE'].iloc[0] 
        adjuntos = []
        
        for hda in group['COD HDA']:# Recorre los cód hda del grupby
            if hda in archivos_por_hda:
                adjuntos.extend(archivos_por_hda[hda])  # Añade los archivos correspondientes al HDA a la lista de adjuntos
        if adjuntos:
            enviar_email(to_addrs, cc_addrs, subject, body, adjuntos)
            #print(to_addrs, cc_addrs, subject, body, adjuntos)
        else:
            print(f"No se encontraron archivos PDF para los correos: {', '.join(to_addrs)}")
            
propias()            
proveedores()
