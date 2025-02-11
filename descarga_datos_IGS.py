"""
Descarga archivos CRX comprimidos de datos GNSS de la red IGS 
desde el servidor de la NASA (https://cddis.nasa.gov/) a una 
carpeta local.

Autor: Ignacio Parada P.
Fecha de Creación: 11 de febrero de 2025

**IMPORTANTE:** El CDDIS migrará su sitio web de cddis.nasa.gov a 
earthdata.nasa.gov entre febrero y junio de 2025.  Las URLs 
en este script deberán ser actualizadas a partir de la fecha de 
migración. 
Para más detalles, consulta: https://cddis.nasa.gov/Web_Unification.html

Este script utiliza credenciales de Earthdata para acceder y descargar 
los archivos. Se recomienda configurar las credenciales como variables de 
entorno por seguridad.

Librerías:
    - requests
    - pathlib
    - datetime

Uso:
    python descarga_datos_IGS.py
"""

import datetime
import os
import time
import requests
from pathlib import Path

# Constantes (URLs y rutas)
NASA_CDDIS_URL = "https://cddis.nasa.gov/archive/gps/data/daily/"
LOCAL_FOLDER = Path(r"C:\Users\IPARADA\Documents\Rutinas\diarias\otras_IGS")

# Listas de estaciones CORS según la frecuencia de actualización (15s o 30s)
# ¡IMPORTANTE! Las siguientes estaciones son solo ejemplos y deben ser
# reemplazadas por las estaciones reales que se deseen descargar.
cors_15seg = ["RDSD00DOM", "SFDM00USA"]  # Ejemplo de CORS con frecuencia de registros de 15 segundos
cors_30seg = ["SANT00CHL", "AGGO00ARG"]  # Ejemplo de CORS con frecuencia de registros de 30 segundos

def generar_urls(año, dia_del_año, estaciones):
    """
    Genera una lista de URLs para los archivos CRX de datos GPS 
    para un día específico y un conjunto de estaciones CORS.

    Args:
        año (int): El año para el cual se generarán las URLs.
        dia_del_año (int): El día del año (1-366) para el cual se 
                            generarán las URLs.
        estaciones (list): Lista de nombres de estaciones CORS.

    Returns:
        list: Una lista de cadenas, donde cada cadena es una URL 
              relativa a la URL base del servidor (ej: "2024/150/24d/RDSD00CHL_R_20241500000_01D_15S_MO.crx.gz").
    """
    urls = []
    for large_name in estaciones:
        if large_name in cors_15seg:
            ruta_archivo = f"{año}/{dia_del_año:03d}/{str(año)[-2:]}d/{large_name}_R_{año}{dia_del_año:03d}0000_01D_15S_MO.crx.gz"
        elif large_name in cors_30seg:
            ruta_archivo = f"{año}/{dia_del_año:03d}/{str(año)[-2:]}d/{large_name}_R_{año}{dia_del_año:03d}0000_01D_30S_MO.crx.gz"
        else:
            print(f"Advertencia: Estación desconocida: {large_name}")
            continue
        urls.append(ruta_archivo)
    return urls

# Obtener fecha actual y calcular la fecha requerida para la descarga
# (se restan 40 días, pero este valor se puede modificar)
hoy = datetime.date.today()
dia_descarga = hoy - datetime.timedelta(days=40)
año_actual = dia_descarga.year
dia_del_año_descarga = dia_descarga.timetuple().tm_yday

# Generar URLs para ambos grupos de estaciones
file_urls_15seg = generar_urls(año_actual, dia_del_año_descarga, cors_15seg)
file_urls_30seg = generar_urls(año_actual, dia_del_año_descarga, cors_30seg)

# Combinar las URLs de ambos grupos
file_urls = file_urls_15seg + file_urls_30seg

# Crear carpeta local
LOCAL_FOLDER.mkdir(parents=True, exist_ok=True)

# Credenciales de Earthdata (desde variables de entorno, más seguro)
EARTHDATA_USERNAME_VAR = "EARTHDATA_USERNAME"
EARTHDATA_PASSWORD_VAR = "EARTHDATA_PASSWORD"

username = os.environ.get(EARTHDATA_USERNAME_VAR)
password = os.environ.get(EARTHDATA_PASSWORD_VAR)

if not username or not password:
    raise ValueError(f"Credenciales de Earthdata no encontradas. Deben estar en las variables de entorno {EARTHDATA_USERNAME_VAR} y {EARTHDATA_PASSWORD_VAR}.")

# Número máximo de reintentos
max_intentos = 3

# Descargar archivos
if __name__ == "__main__":
    for file_url in file_urls:
        remote_url = f"{NASA_CDDIS_URL}{file_url}"
        local_path = LOCAL_FOLDER / file_url.split('/')[-1]

        if local_path.exists():
            print(f"Archivo {local_path} ya existe. Verificando integridad...")
            # Obtener tamaño remoto para validar integridad
            response_head = requests.head(remote_url, auth=(username, password))
            if response_head.status_code == 200:
                remote_size = int(response_head.headers.get('Content-Length', 0))
                local_size = local_path.stat().st_size
                if local_size == remote_size:
                    print(f"Archivo {local_path} está completo. Saltando...")
                    continue
                else:
                    print(f"Tamaño inconsistente, volviendo a descargar {local_path}...")
            else:
                print(f"Error al verificar archivo remoto: {remote_url}")
                continue
        intentos = 0
        descargado = False
        while not descargado and intentos < max_intentos:
            try:
                print(f"Descargando {remote_url}...")
                response = requests.get(remote_url, stream=True, auth=(username, password))
                response.raise_for_status()

                with local_path.open('wb') as local_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        local_file.write(chunk)

                # Verificar tamaño después de la descarga
                remote_size = int(response.headers.get('Content-Length', 0))
                local_size = local_path.stat().st_size
                if local_size == remote_size:
                    print(f"Archivo {local_path} descargado correctamente.")
                    descargado = True
                else:
                    print(f"Error: El archivo {local_path} está incompleto. Tamaño inconsistente.")
                    intentos += 1

            except requests.RequestException as e:
                print(f"Error al descargar {remote_url}: {e}.  Código de estado: {response.status_code if hasattr(response, 'status_code') else 'Desconocido'}")
                intentos += 1
        if not descargado:
            print(f"Error: No se pudo descargar {remote_url} después de {max_intentos} intentos.")
    print("Descarga completa.")