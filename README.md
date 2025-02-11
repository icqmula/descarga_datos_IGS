# Descarga Datos GNSS IGS

Este script en Python descarga archivos CRX comprimidos de datos GNSS de la red IGS desde el servidor de la NASA (https://cddis.nasa.gov/) a una carpeta local.

**IMPORTANTE:** El CDDIS migrar� su sitio web de cddis.nasa.gov a earthdata.nasa.gov entre febrero y junio de 2025. Las URLs en este script deber�n ser actualizadas a partir de la fecha de migraci�n. Para m�s detalles, consulta: https://cddis.nasa.gov/Web_Unification.html

Este script utiliza credenciales de Earthdata para acceder y descargar los archivos. Se recomienda configurar las credenciales en un archivo `.netrc` por seguridad.

## Autor

Ignacio Parada P.

## Fecha de Creaci�n

11 de febrero de 2025

## Librer�as

- requests
- pathlib
- datetime

## Uso

```bash
python descarga_datos_IGS.py


Requisitos
Python 3.x
Librer�as listadas en "Librer�as" (se pueden instalar con pip install requests)
Credenciales de Earthdata configuradas en un archivo .netrc

Configuraci�n
Credenciales de Earthdata:

Crea un archivo .netrc en tu directorio home (o donde tu sistema lo requiera).
A�ade las siguientes l�neas, reemplazando tu_usuario_earthdata y tu_contrase�a_earthdata con tus credenciales reales:
machine cddis.nasa.gov
login tu_usuario_earthdata
password tu_contrase�a_earthdata
Ruta de Descarga:

Modifica la variable LOCAL_FOLDER en el script para especificar la carpeta local donde se guardar�n los archivos descargados.
Estaciones CORS:

Las listas cors_15seg y cors_30seg contienen ejemplos de estaciones CORS. Debes reemplazarlas con las estaciones reales que deseas descargar.
Funcionamiento
El script realiza los siguientes pasos:

Calcula la fecha de descarga restando 40 d�as a la fecha actual (este valor se puede modificar).
Genera las URLs de los archivos CRX para las estaciones CORS especificadas.
Crea la carpeta local si no existe.
Descarga los archivos CRX, verificando su integridad y reintentando la descarga en caso de errores.