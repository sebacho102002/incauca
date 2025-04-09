===========================================
Manual de Uso: Script Recibir Correos
===========================================

Descripción:
------------
Este script automatiza la extracción de códigos desde correos electrónicos no leídos y su búsqueda en la 
plataforma Manglar mediante un navegador web controlado por Selenium.

Características:
---------------
1. Escanea correos no leídos desde Microsoft Outlook.
2. Extrae códigos específicos y los busca en la plataforma Manglar.
3. Notifica al usuario mediante ventanas emergentes sobre el progreso y resultados.

Requisitos:
-----------
1. **Python 3.9+**.
2. Librerías necesarias:
   - selenium
   - tkinter
   Comando para instalar:
       pip install selenium
3. Microsoft Outlook configurado.
4. Webdriver para Chrome compatible con tu versión de navegador:
   - Descárgalo desde: https://chromedriver.chromium.org/downloads

Configuración:
--------------
1. Configura las rutas y credenciales en el archivo `config.py`:
   - `webdriver_path`: Ruta al ChromeDriver.
   - `Correo_m`: Correo electrónico para iniciar sesión en Manglar.
   - `Contra_m`: Contraseña de la cuenta.

Uso del Script:
---------------
1. Configura el archivo `config.py` con las credenciales y rutas necesarias.
2. Ejecuta el script:
   ```bash
   python main.py
3. El script realizará lo siguiente:
    Buscará correos no leídos en Outlook y extraerá códigos.
    Accederá a Manglar mediante Chrome y buscará los códigos extraídos.
    