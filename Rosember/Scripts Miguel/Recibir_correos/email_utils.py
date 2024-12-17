import win32com.client as win32
import re
import pandas as pd
import os

class EmailsUtil:
    def __init__(self):
        self.ruta_guardado = r'C:\Geodata\Mapas_Despoblacion\Envio mapas zonas\fechas\codigos_y_fechas.xlsx'
    
    def codsia_outlook(self):
        if os.path.exists(self.ruta_guardado):
            os.remove(self.ruta_guardado)
            print(f"Archivo existente {self.ruta_guardado} eliminado.")
        
        outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
        inbox = outlook.GetDefaultFolder(6)
        codigos = []
        datos = []

        while True:
            messages = inbox.Items.Restrict("[Unread] = true AND [Subject] = 'Image processing complete'")
            if messages.Count == 0:
                break

            for message in messages:
                try:
                    codsia = re.search(r'Processing completed for (\w+)', message.Body)
                    f_vuelo = re.search(r'Flight Date: (\d{2}/\d{2}/\d{4})', message.Body)
                    
                    if codsia and f_vuelo:
                        codigo = codsia.group(1)
                        fecha_vuelo = f_vuelo.group(1)
                        fecha_correo = message.ReceivedTime.strftime('%d/%m/%Y')
                        codigos.append(codigo)
                        datos.append({
                            'Codigo': codigo,
                            'Fecha Correo': fecha_correo,
                            'Fecha Vuelo': fecha_vuelo
                        })
                        message.UnRead = False
                except Exception as e:
                    print(f'Error al procesar el mensaje: {e}')
        
        df = pd.DataFrame(datos)
        df.to_excel(self.ruta_guardado, index=False)
        print(f"Datos exportados a {self.ruta_guardado}")

        return codigos
