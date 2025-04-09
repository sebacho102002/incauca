======================================
Manual de Uso: Script de Envío de Correos
======================================

Descripción:
------------
Este script automatiza el envío de correos electrónicos mediante Microsoft Outlook. 
Permite procesar datos desde archivos Excel para generar archivos separados por 
zonas y proveedores, y enviarlos como correos electrónicos con adjuntos.

Características:
---------------
- Procesa dos archivos Excel:
  1. Archivo principal: Contiene información sobre suertes y haciendas.
  2. Archivo de correos: Lista los proveedores y sus respectivas haciendas.
- Genera archivos Excel separados para cada zona y proveedor.
- Envío de correos:
  - **Zonas**: Mensajes generales con datos de la zona.
  - **Proveedores**: Correos personalizados con la información específica del proveedor.
- Notifica las haciendas que no tienen un proveedor asignado.

Requisitos:
-----------
1. Tener instalado Python 3.9 o superior.
2. Instalar las siguientes librerías:
   - pandas
   - pywin32
   Comando para instalar: 
       pip install pandas pywin32
3. Tener Microsoft Outlook configurado con una cuenta activa.
4. Estructura de los archivos Excel:
   - Archivo principal:
     - Columnas requeridas: `Zona`, `Hacienda`, `Tenencia`, `Ult.Cor/Siem`.
   - Archivo de correos:
     - Columnas requeridas: `Proveedor`, `Hacienda`, `Correo Principal`, `CC`.

Uso del Script:
---------------
1. Ejecutar el script:
   python envio_correos.py
2. Aparecerá una ventana emergente para seleccionar el archivo principal (Excel).
3. Confirmar si deseas proceder con el envío de correos.
4. El script procesará los datos, generará los archivos necesarios y enviará los correos.
5. Se notificará cualquier error o las haciendas sin proveedor asignado.

Configuraciones Personalizables:
--------------------------------
1. Rutas de los archivos:
   - Cambiar la ruta predeterminada para el archivo principal en la función `seleccionar_archivo`.
   - Verificar la ruta del archivo de correos:
       correos_path = 'C:/Geodata/Mapas_Despoblacion/Envio Programa vuelo/Correos.xlsx'

2. Cuerpo y asunto de los correos:
   - Modificar las variables `subject` y `body` para personalizar los mensajes.

Errores Comunes:
----------------
1. "Archivo no encontrado":
   - Asegúrate de seleccionar un archivo Excel válido.
2. Error en Outlook:
   - Verifica que Microsoft Outlook esté configurado correctamente.
3. Haciendas faltantes:
   - Revisa y actualiza el archivo de correos con las haciendas que faltan.

Mantenimiento:
--------------
1. Verifica regularmente que las rutas de los archivos sean válidas.
2. Mantén actualizada la lista de correos en el archivo correspondiente.
3. Asegúrate de que los datos de los archivos Excel cumplen con la estructura requerida.

======================================
Fin del Manual
======================================
