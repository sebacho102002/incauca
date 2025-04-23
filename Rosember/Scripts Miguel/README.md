# Manual de Uso: Aplicación de Procesos AP

## Descripción
Esta aplicación de escritorio con interfaz gráfica (Tkinter) permite ejecutar diversos scripts de automatización asociados a los procesos del área de Agricultura de Precisión (AP). Cada botón lateral corresponde a una categoría de trabajo y muestra los scripts disponibles para ejecutar.

Incluye integración con Microsoft Outlook, procesamiento de archivos Excel y uso de hilos para mantener la interfaz responsiva.

---

## Estructura General

- **App.py**: Archivo principal que lanza la aplicación gráfica.
- **Carpetas de scripts**: Cada carpeta dentro de `Scripts Miguel` contiene un `main.py` ejecutable al presionar un botón.
  - Ej: `Scripts Miguel/Recibir_correos/main.py`, `Scripts Miguel/Annotations/main.py`, etc.
- **logo.ico**: Icono que se usará al compilar la aplicación a `.exe`.

---

## Requisitos

1. Python 3.9 o superior instalado.
2. Microsoft Outlook configurado si se utilizan scripts que envían correos.
3. Librerías necesarias:
   ```bash
   pip install pandas openpyxl pywin32
   ```
4. Estructura de carpetas:
   ```
   C:/Geodata/Mapas_Despoblacion/Scripts Miguel/
       |-- App.py
       |-- cana.ico
       |-- Recibir_correos/
       |-- Annotations/
       |-- Enviar_correos_mapas/
       ...
   ```

---

## Uso del Programa

1. Ejecutar el script:
   ```bash
   python App.py
   ```

2. Se abrirá una interfaz con botones laterales (Despoblación, Buscar, etc.).
3. Al seleccionar una categoría, se mostrarán botones para ejecutar scripts específicos.
4. Presiona "Ejecutar" para lanzar el script correspondiente. Se mostrará un mensaje al finalizar.

---

## Compilación a .EXE (distribución)

### Comando:
```bash
pyinstaller --noconfirm --onefile --windowed --icon=cana.ico App.py
```

### Explicación:
- `--onefile`: genera un único archivo `.exe`.
- `--windowed`: oculta la consola negra.
- `--icon=cana.ico`: icono personalizado.

### Resultado:
El archivo ejecutable estará en:
```plaintext
dist/App.exe
```

---

## Actualizaciones al Script

### Si realizas cambios en `App.py` o en los scripts:
1. Guarda todos los archivos modificados.
2. Abre la terminal en la ruta del proyecto:
   ```bash
   cd /c/Geodata/Mapas_Despoblacion/Scripts Miguel
   ```
3. Vuelve a ejecutar el comando de compilación:
   ```bash
   pyinstaller --noconfirm --onefile --windowed --icon=cana.ico App.py
   ```
4. El nuevo `.exe` se generará con las modificaciones aplicadas.

---

## Recomendaciones
- Asegúrate de cerrar el `.exe` antes de recompilar.
- Mantén organizada la estructura de carpetas.
- Verifica que todos los `main.py` de las subcarpetas sean ejecutables y estén probados.

---

**Fin del Manual**