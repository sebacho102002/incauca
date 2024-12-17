import geopandas as gpd 
import pandas as pd 
from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox
import time

class GeoDataProcessor:
    def __init__(self, rSte, rXlsx, key='CODSIA', sheet_name=0, ste_div=True):
        self.rSte = rSte
        self.rXlsx = rXlsx
        self.key = key
        self.sheet_name = sheet_name
        self.ste_div = ste_div
        self.rutaS = "C:/Geodata/Mapas_Despoblacion/Envio Programa vuelo/"

    def process_data(self):
        try: 
            # Cargar datos con Geopandas
            suerte_gdf = gpd.read_file(self.rSte)
            
            # Cargar datos del archivo Excel y asegurar que la columna CODSIA sea texto
            logi_df = pd.read_excel(self.rXlsx, sheet_name=self.sheet_name, dtype={self.key: str})

            # Filtrar suerte_gdf para mantener solo los polígonos cuyos CODSIA están en logi_df
            if logi_df[self.key].nunique() == 1:
                codsia = logi_df[self.key].iloc[0]
                suerte_gdf = suerte_gdf[suerte_gdf[self.key] == codsia] 
            else:
                suerte_gdf = suerte_gdf[suerte_gdf[self.key].isin(logi_df[self.key])]

            # Realizar el join
            result_gdf = suerte_gdf.merge(logi_df, left_on=self.key, right_on=self.key, how='left', suffixes=('', '_y'))

            if not self.ste_div:
                result_gdf = result_gdf.dropna(subset=[self.key])

            # Filtrar para mantener solo los polígonos que coinciden
            result_gdf = result_gdf.dropna(subset=[f"{self.key}"])

            # Renombrar columnas para cumplir con la limitación de 10 caracteres de los shapefiles
            result_gdf.columns = [col[:10] for col in result_gdf.columns]

            # Convertir columnas datetime a cadenas de texto
            for col in result_gdf.select_dtypes(include=['datetime64']).columns:
                result_gdf[col] = result_gdf[col].dt.strftime('%Y-%m-%d')



            # Datos para nombre del archivo final
            hoy = datetime.now()
            anio = hoy.isocalendar()[0]
            numSem = hoy.isocalendar()[1]
            wk = f"{anio}{numSem}"

            # Guardar la capa resultante en un archivo shapefile
            output_shapefile = os.path.join(self.rutaS, f"Drone_W_{wk}.shp")
            result_gdf.to_file(output_shapefile)

            return output_shapefile
        
        except Exception as e:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
            root.destroy()
            return None

def main():
    rSte = r"\\INDICA07\Geodata\Incauca_Gen\WGS84\shp\ste.shp"
    rXlsx = "C:/Geodata/Mapas_Despoblacion/Envio Programa vuelo/join_drone.xlsx"

    # Crear instancia de GeoDataProcessor
    processor = GeoDataProcessor(rSte, rXlsx, ste_div=True)
    
    # Procesar datos
    output_file = processor.process_data()

    if output_file:
        # Imprimir información de salida
        print(f"INFO: Capa '{output_file}' generada y almacenada con éxito en '{processor.rutaS}'.")
    else:
        print("ERROR: No se pudo generar la capa debido a un error.")

if __name__ == "__main__":
    main()
