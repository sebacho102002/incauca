Este script lee rutas especificas, por lo tanto, si va a cambiar la ubicacion de los archivos tambien debe de cambiar las rutas dentro de este script.

Logica al usuario:

este script realiza la revisión del excel donde se encuentran las suertes con edad suficiente para vuelo. filtra el archivo separando cada uno por zonas y enviandolo por correo a cada uno de los jefes de la zona. las suertes que son de proveedores tambien se le envían a cada uno de los correos de los proveedores descritos en la base de datos de los correos (debe de coincidor el nombre de la hacienda del excel con el de la base de datos, sino va a tener error al enviar), generando una nueva carpeta dentro de la anterior que se llamaría "proveedores". genera informe de los correos enviados y genera un archivo para cada uno.
Primero el script realiza el ETL (filtro y generacion de nuevos archivos) antes de enviar por correo para que el usuario tenga la oprtunidad de revisar los archivos creados y así poder presionar el botón de envío por correo


Logica computacional: 

sl script utiliza libreria win32 para el envío de archivos mediante correo electronico el cual es el que está anclado principalmente al pc.
Primeramente hace un filtrado de el archivo excel, filtrando por tipo de zona y generando un nuevo archivo por cada zona. dentro del script hay un espacio donde están los correos de todos los jefes, donde automaticamente se envian a esos correos asociados los archivos correspondientes a cada zona. paralelamente tambien se crean otro archivos en una carpeta nueva (dir creada por codigo) donde se guardan los datos que van a cada proveedor para autorizacion de vuelo. para los proveedores, como son varios, hay una base de datos donde asociamos cada nombre de la hacienda con un correo. el script compara el nombre de la zona con el nombre de la hacienda entre uno y otro excel, cogiendo los correos asociados y enviando los datos correspondientes. 

tener cuidado al cambiar las rutas especificas para el correcto funcionamiento del prpograma. 