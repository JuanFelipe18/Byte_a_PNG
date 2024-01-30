from concurrent.futures import ThreadPoolExecutor
from tkinter import font, filedialog
from base64 import b64decode
from shutil import rmtree
import tkinter as tk
import pandas as pd
import time
import sys
import os

class Orden:
    def __init__(self):
        self.ventana_bienvenida = tk.Tk()
        self.ventana_bienvenida.title("Codificador GCM")
        #self.imagen = tk.PhotoImage(file=self.resolver_ruta("logo.png"))  # Reemplaza con la ruta de tu imagen
        self.imagen = tk.PhotoImage(file="logo.png")  # Reemplaza con la ruta de tu imagen
        self.imagen = self.imagen.subsample(6)  # Ajusta el factor de submuestreo según sea necesario
        self.fuente_personalizada = font.Font(family="Cambria Math", size=16)
        self.fuente_personalizada2 = font.Font(family="Sitka Subheading", size=16)
        self.setup_interfaz()

    def setup_interfaz(self):
        label_imagen = tk.Label(self.ventana_bienvenida, image=self.imagen)
        label_imagen.pack()

        etiqueta_bienvenida = tk.Label(self.ventana_bienvenida, text="GENERAR IMAGENES", font=self.fuente_personalizada)
        etiqueta_bienvenida.pack(padx=10, pady=0)

        texto_adicional_1 = tk.Label(self.ventana_bienvenida, text="Versión 1.0",
                                    font=font.Font(family="Courier New", size=12))
        texto_adicional_1.pack()

        texto_adicional_2 = tk.Label(self.ventana_bienvenida,
                                     text="Grupo de Acceso a la Informacion y \nProtección de Datos Personales",
                                     font=font.Font(family="Courier New", size=12))
        texto_adicional_2.pack()

        texto_adicional_3 = tk.Label(self.ventana_bienvenida, text="Autor: Juan Felipe Martín Martínez",
                                     font=font.Font(family="Courier New", size=12))
        texto_adicional_3.pack()

        texto_adicional_4 = tk.Label(self.ventana_bienvenida,
                                     text="PROGRAMA DE USO EXCLUSIVO \nREGISTRADURIA NACIONAL DEL \nESTADO CIVIL",
                                     font=self.fuente_personalizada2)
        texto_adicional_4.pack()

        texto_adicional_5 = tk.Label(self.ventana_bienvenida, text="2023",
                                     font=font.Font(family="Courier New", size=12))
        texto_adicional_5.pack()

        self.boton_iniciar = tk.Button(self.ventana_bienvenida, text="Seleccionar archivo CSV", command=self.generar_imagenes)
        self.boton_iniciar.pack(pady=20)

    def resolver_ruta(self, archivo):
        if hasattr(sys, '_MEIPASS'):  # Verifica si estamos en el entorno empaquetado
            return os.path.join(sys._MEIPASS, archivo)
        else:
            return os.path.join(os.path.abspath('.'), archivo)

    def progress_bar(self):
            self.ventana_progreso = tk.Toplevel()
            self.ventana_progreso.title("ProgressBar")
            self.ventana_progreso.geometry("300x100")

            self.label = tk.Label(self.ventana_progreso, text="Procesando...", font=("Arial", 22))
            self.label.place(x=40, y=10)
            self.ventana_progreso.update() 

    def process_chunk(self, chunk):
        processed = []
        errors = []
        files_processed = 0
        for i, row in chunk.iterrows():
            try:
                imagen = b64decode(row['PHOTO'])
                nombre_archivo = f"{str(row['NUIP_NIP']).replace('.0', '').zfill(10)}-{row['LOG_ID']}-{row['AUTHENT_RESULT']}-{str(row['SCORE']).replace('.0', '')}.jpg"
                ruta = os.path.join(directorio_imagenes, nombre_archivo)
                with open(ruta, "wb") as file:
                    file.write(imagen)
                processed.append(i)
            except Exception as e:
                errors.append(f"Error en el registro {i}, con NUIP {row['NUIP_NIP']}: {str(e)}")
        return processed, errors, files_processed

    def generar_imagenes(self):
        global directorio_imagenes, files_processed

        directorio_imagenes = os.path.join(os.getcwd(), "Imágenes generadas")
        if os.path.exists(directorio_imagenes):
            rmtree(directorio_imagenes)
        os.makedirs(directorio_imagenes)

        file_path = filedialog.askopenfilename()
        inicio_tiempo = time.time()
        chunk_size = 10000  # Define el tamaño del chunk adecuado según tus necesidades

        # Lee el archivo CSV en chunks
        chunks = pd.read_csv(file_path, delimiter=';', chunksize=chunk_size)
        processed_records = []
        error_records = []

        self.progress_bar()

        with ThreadPoolExecutor(max_workers=4) as executor:  # Puedes ajustar el número de workers
            futures = []
            for chunk in chunks:
                future = executor.submit(self.process_chunk, chunk)
                futures.append(future)

            for future in futures:
                processed, errors, files_processed = future.result()
                processed_records.extend(processed)
                error_records.extend(errors)

        fin_tiempo = time.time()
        tiempo_transcurrido = fin_tiempo - inicio_tiempo
        with open(os.path.join(os.getcwd(), "Tiempo.txt"), "w") as archivo_tiempo:
            archivo_tiempo.write(str(tiempo_transcurrido))
        self.mostrar_ventana_final()
            
    def mostrar_ventana_final(self):
        ventana_final = tk.Toplevel()
        ventana_final.title("Finalizo")

        label_imagen = tk.Label(ventana_final, image=self.imagen)
        label_imagen.pack()

        etiqueta_final = tk.Label(ventana_final, text="¡Proceso finalizado con éxito!", font=self.fuente_personalizada)
        etiqueta_final.pack(padx=10, pady=5)

        boton_aceptar = tk.Button(ventana_final, text="Aceptar", command=self.cerrar_programa)
        boton_aceptar.pack(pady=5)

        ventana_final.protocol("WM_DELETE_WINDOW", self.cerrar_programa)

    def cerrar_programa(self):
        self.ventana_bienvenida.quit()

if __name__ == "__main__":
    app = Orden()
    app.ventana_bienvenida.mainloop()
