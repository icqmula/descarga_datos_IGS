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

## Instalación

1. Clona este repositorio: `git clone https://github.com/tu_usuario/descarga-datos-gnss.git`
2. Instala las librerías necesarias: `pip install requests pathlib`

## Uso

```bash
python descarga_datos_IGS.py
