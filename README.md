# Descarga de Datos GNSS de la Red IGS

Este script en Python descarga archivos CRX comprimidos de datos GNSS (Global Navigation Satellite System) de la red IGS (International GNSS Service) desde el servidor de la NASA (CDDIS) a una carpeta local.  Estos datos son utilizados en geodesia, geofísica y otras aplicaciones científicas para obtener información precisa sobre la posición de puntos en la Tierra.

## Características

* Descarga de datos de estaciones CORS (Continuously Operating Reference Stations) de la red IGS.
* Soporte para estaciones con diferentes frecuencias de registro (15 segundos y 30 segundos).
* Autenticación con credenciales de Earthdata.
* Verificación de la integridad de los archivos descargados.
* Reintentos automáticos en caso de errores de descarga.

## Requisitos

* Python 3.x
* Librerías `requests` y `pathlib` (se pueden instalar con  `pip install requests pathlib`)
* Credenciales de Earthdata
* Crea un archivo llamado .netrc y guardalo en el home (carpeta de usuario de windows) el archivo debe contener la siguiente información:
```bash
machine urs.earthdata.nasa.gov
login tu_usuario_earthdata
password tu_contraseña_earthdata
```
* Variables de entorno:
Define las variables de entorno del sistema EARTHDATA_USERNAME y EARTHDATA_PASSWORD con tus credenciales.
* Ruta de descarga: Modifica la variable LOCAL_FOLDER en el script para especificar la carpeta local donde se guardarán los archivos descargados.

## Instalación

1. Clona este repositorio: `git clone https://github.com/icqmula/descarga_datos_IGS.git`
2. Instala las librerías necesarias: `pip install requests pathlib`

## Uso

```bash
python descarga_datos_IGS.py
```


