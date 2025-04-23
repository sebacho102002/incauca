======================================
Manual de Uso: Script de Envio de Correos - Incauca
======================================

Descripcion:
------------
Este script automatiza el procesamiento de datos y el envio de correos electronicos mediante Microsoft Outlook. Procesa informacion desde archivos Excel para generar reportes por zonas y proveedores, conservando el formato original del archivo base, y los envia como archivos adjuntos en correos personalizados.

Caracteristicas:
---------------
- Procesa dos archivos Excel:
  1. Archivo principal: Contiene informacion sobre suertes, zonas, haciendas, edades y variedad.
  2. Archivo de correos: Contiene la lista de proveedores y sus respectivas haciendas, junto con los correos de contacto.

- Genera archivos Excel con formato conservado:
  - Uno por cada zona.
  - Uno por cada proveedor con tenencia igual a 51.

- Ajusta automaticamente el ancho de las columnas "Nombre" y "Zona" para mejor visualizacion.
- Mantiene los ceros a la izquierda en los codigos de hacienda.
- Envia correos por cada zona y proveedor con mensajes personalizados.
- Notifica si existen haciendas sin proveedor asignado.

Requisitos:
-----------
1. Python 3.9 o superior.
2. Librerias requeridas:
   - pandas
   - openpyxl
   - pywin32
   Comando para instalarlas:
       pip install pandas openpyxl pywin32
3. Microsoft Outlook instalado y configurado.

Estructura esperada de archivos Excel:
--------------------------------------
- **Archivo principal**:
  - Hoja: "Hoja1"
  - Columnas requeridas: `Zona`, `Hacienda`, `Tenencia`, `Nombre`, `Ult.Cor/Siem`, `Edad`, `Variedad`, etc.

- **Archivo de correos**:
  - Columnas requeridas: `Proveedor`, `Hacienda`, `Correo Principal`, `CC`

Uso del Script:
---------------
1. Ejecutar el script:
   python envio_correos.py
2. Seleccionar el archivo Excel principal cuando se solicite.
3. El script creara los archivos separados y preguntara si deseas enviar los correos.
4. Se enviaran los correos desde Outlook, incluyendo los archivos adjuntos.
5. Se mostraran mensajes de exito o advertencia al finalizar.

Personalizacion:
----------------
1. Modificar el cuerpo y asunto de los correos:
   - Buscar las variables `subject` y `body` dentro del script.
2. Cambiar la ruta predeterminada en la funcion `seleccionar_archivo()`.

Errores comunes:
----------------
1. **Archivo no encontrado**:
   - Verifica que seleccionaste un archivo Excel valido.
2. **Outlook no responde**:
   - Asegurate de tener Outlook abierto y configurado.
3. **Datos incorrectos o faltantes**:
   - Revisa que los archivos contengan las columnas requeridas.

Mantenimiento:
--------------
1. Revisa las rutas y nombres de archivos antes de ejecutar.
2. Asegura la consistencia de nombres en las zonas y haciendas.
3. Actualiza regularmente el archivo de correos con nuevas haciendas o proveedores.

======================================
Fin del Manual
======================================