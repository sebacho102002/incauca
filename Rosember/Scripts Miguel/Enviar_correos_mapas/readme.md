===========================================
Manual de Uso: Script Enviar Correos Mapas
===========================================

Descripción:
------------
Este script automatiza el envío de correos electrónicos con archivos PDF adjuntos 
relacionados con mapas de zonas y proveedores. Los datos de los correos y los archivos 
se organizan en hojas de un archivo Excel y carpetas locales específicas.

Características:
---------------
1. **Procesamiento de dos tipos de correos**:
   - **Zonas Propias**: Envía correos con información específica de cada zona.
   - **Proveedores**: Envía correos personalizados a proveedores con información específica de sus haciendas.
2. **Gestión de archivos PDF**:
   - Identifica automáticamente los archivos PDF asociados a cada zona o proveedor.
3. **Envío de correos electrónicos**:
   - Integra Microsoft Outlook para automatizar el envío.
   - Soporta múltiples destinatarios y copias en cada correo.

Requisitos:
-----------
1. **Python 3.9+**.
2. Librerías necesarias:
   - pandas
   - pywin32
   Comando para instalar:
       pip install pandas pywin32
3. **Microsoft Outlook** configurado con una cuenta activa.
4. Estructura requerida:
   - **Archivo Excel** con las hojas `Propias` y `Proveedores`, que incluyen:
     - Columnas necesarias:
       - **Propias**: `ZONA`, `CORREO PARA`, `CON COPIA A:`, `ASUNTO`, `CUERPO MENSAJE`.
       - **Proveedores**: `COD HDA`, `CORREO PARA`, `CON COPIA A:`, `ASUNTO`, `CUERPO MENSAJE`.
   - **Carpetas locales**:
     - Carpeta principal: `C:/Geodata/Mapas_Despoblacion/Envio mapas zonas`.
     - Subcarpeta semanal: `Zonas 2025XX` (XX es el número de semana actual).

Estructura del programa:
------------------------
1. **Cargar datos desde el archivo Excel**:
   - Lee las hojas `Propias` y `Proveedores` para obtener la configuración de correos y mensajes.
2. **Procesamiento de zonas propias**:
   - Identifica las carpetas asociadas a cada zona.
   - Busca archivos PDF y los adjunta a los correos correspondientes.
3. **Procesamiento de proveedores**:
   - Agrupa los datos por correo electrónico.
   - Busca archivos PDF asociados a las haciendas de cada proveedor.
4. **Envío de correos electrónicos**:
   - Envía los correos con los archivos adjuntos correspondientes a cada destinatario.

Uso del Script:
---------------
1. Asegúrate de que la estructura de carpetas y el archivo Excel cumplen con los requisitos.
2. Ejecuta el script:
   ```bash
   python enviar_correos_mapas.py
