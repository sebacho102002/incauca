===========================================
Manual de Uso: Script Crear Polígonos
===========================================

Descripción:
------------
Este script utiliza datos geoespaciales y de Excel para generar una nueva capa geográfica (shapefile) 
que contiene información procesada de polígonos. Está diseñado para facilitar el manejo de datos 
geográficos y su integración en flujos de trabajo agrícolas.

Características:
---------------
1. **Integración de datos geográficos y tabulares**:
   - Realiza un "join" entre un archivo shapefile y un archivo Excel, usando una clave común (`CODSIA`).
2. **Filtrado y limpieza de datos**:
   - Filtra polígonos basándose en los valores de la clave (`CODSIA`) proporcionados en el archivo Excel.
   - Limpia los datos eliminando valores nulos y ajustando los nombres de columnas.
3. **Generación de shapefiles**:
   - Crea un nuevo archivo shapefile con la información procesada y nombres de columnas compatibles con la limitación de 10 caracteres.
4. **Interfaz amigable**:
   - Notifica errores mediante ventanas emergentes para una mejor experiencia del usuario.

Requisitos:
-----------
1. **Python 3.9+**.
2. Librerías necesarias:
   - geopandas
   - pandas
   - tkinter
   - openpyxl
   Comando para instalar:
       pip install geopandas pandas tkinter openpyxl
3. **Archivos necesarios**:
   - Archivo shapefile (`.shp`) con la geometría de los polígonos.
   - Archivo Excel (`.xlsx`) con los datos tabulares que serán vinculados.

Estructura de los archivos:
---------------------------
1. **Shapefile**:
   - Ruta predeterminada: `\\INDICA07\Geodata\Incauca_Gen\WGS84\shp\ste.shp`.
   - Debe contener la clave `CODSIA`.
2. **Archivo Excel**:
   - Ruta predeterminada: `C:/Geodata/Mapas_Despoblacion/Envio Programa vuelo/join_drone.xlsx`.
   - Columnas requeridas:
     - `CODSIA`: Clave para realizar el "join".
     - Otras columnas adicionales serán agregadas al shapefile resultante.

Uso del Script:
---------------
1. **Ejecutar el script**:
   - Ejecuta el script desde la línea de comandos:
       python crear_poligonos.py
2. **Procesamiento**:
   - El script cargará el shapefile y el archivo Excel, realizará el "join" y generará un nuevo shapefile.
3. **Resultado**:
   - El shapefile generado será almacenado en la carpeta:
       `C:/Geodata/Mapas_Despoblacion/Envio Programa vuelo/`
   - Nombre del archivo generado: `Drone_W_{semana_actual}.shp`.

Configuraciones Personalizables:
--------------------------------
1. **Rutas de entrada**:
   - Modifica las rutas `rSte` y `rXlsx` en el código para ajustar las ubicaciones de los archivos.
     ```python
     rSte = r"\\INDICA07\Geodata\Incauca_Gen\WGS84\shp\ste.shp"
     rXlsx = "C:/Geodata/Mapas_Despoblacion/Envio Programa vuelo/join_drone.xlsx"
     ```
2. **Clave de unión**:
   - Cambia la clave de unión modificando el valor de `key` en la clase `GeoDataProcessor`.

Errores Comunes:
----------------
1. **Error al cargar archivos**:
   - Verifica que las rutas de los archivos sean correctas.
   - Asegúrate de que los archivos existen en las ubicaciones especificadas.
2. **Error al realizar el "join"**:
   - Asegúrate de que la clave `CODSIA` está presente tanto en el shapefile como en el archivo Excel.
3. **Error en la generación del shapefile**:
   - Verifica que tienes permisos para escribir en la carpeta de salida.

Mantenimiento:
--------------
1. **Actualización de rutas**:
   - Asegúrate de que las rutas a los archivos shapefile y Excel son correctas y actualizadas.
2. **Validación de datos**:
   - Revisa los datos en los archivos de entrada para evitar errores de procesamiento.
3. **Pruebas periódicas**:
   - Realiza pruebas periódicas para garantizar que el script funciona correctamente con nuevos datos.

===========================================
Fin del Manual
===========================================
