## Servidor de nombres de recursos de archivo (UDP)

Proceso que mantiene una lista publicable de archivos de una carpeta local, con TTL por archivo, sincronización periódica y un servidor UDP que responde si un archivo está disponible (ACK/NACK) en JSON.

### Requisitos

- Python 3.9 o superior (macOS ya lo trae normalmente como `python3`).

### Estructura general

- `main.py`: punto de entrada (CLI).
- `app/config.py`: manejo de configuración y warm-start en `config.json`.
- `app/scanner.py`: escaneo periódico de la carpeta (alta/baja de archivos y prompts).
- `app/udp_server.py`: servidor UDP en puerto 50000.
- `app.log`: archivo de logs.

### Arranque rápido (recomendado para pruebas)

1) Crear carpeta y archivo de prueba (opcional, ya se incluye un ejemplo en la guía de uso):
```bash
mkdir -p "/Users/<TU_USUARIO>/Desktop/DNS_test"
echo "hola" > "/Users/<TU_USUARIO>/Desktop/DNS_test/archivo.txt"
```

2) Ejecutar el servidor apuntando a esa carpeta (te pedirá publicar s/n y TTL si no hay `config.json`):
```bash
python3 /Users/<TU_USUARIO>/Desktop/DNS/main.py --folder "/Users/<TU_USUARIO>/Desktop/DNS_test"
```
Cuando veas en consola: "Servidor iniciado. UDP en puerto 50000." el servidor está listo.

3) En otra terminal, consulta por UDP si un archivo está disponible:
```bash
python3 -c 'import socket, json; s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.settimeout(3); s.sendto(json.dumps({"filename":"archivo.txt"}).encode(), ("127.0.0.1",50000)); print(s.recvfrom(4096)[0].decode())'
```
Verás una respuesta JSON:
- ACK: {"status":"ACK","filename":"archivo.txt","ttl":300}
- NACK: {"status":"NACK","filename":"archivo.txt"}

### Uso detallado (CLI)

```bash
python3 main.py [--folder "/ruta/absoluta"] [--config "/ruta/config.json"] [--scan-interval 300]
```

- `--folder`: ruta absoluta de la carpeta a vigilar. Si se omite y no hay folder en `config.json`, el programa la pedirá por consola.
- `--config`: ruta al archivo de configuración (por defecto `config.json` en el directorio del proyecto).
- `--scan-interval`: segundos entre escaneos (por defecto 300 = 5 minutos). Durante el escaneo, el hilo detecta archivos nuevos y pedirá si publicar y su TTL; también elimina los que ya no existan.

### Configuración (warm-start) en `config.json`

Formato:
```json
{
  "folder": "/ruta/absoluta/a/la/carpeta",
  "files": {
    "nombre.ext": { "publish": true, "ttl": 300 }
  }
}
```
- Si existe, se carga al inicio y se sincroniza con el contenido real de la carpeta.
- Cada escaneo persiste cambios (altas/bajas) en el mismo archivo.
- Puedes editar manualmente `publish` y `ttl` con el servidor detenido, y volver a iniciar.

### Servidor UDP

- Escucha en `0.0.0.0:50000` (UDP).
- Solicitud (JSON): `{"filename":"nombre.ext"}`
- Respuestas:
  - ACK: `{"status":"ACK","filename":"nombre.ext","ttl":<segundos>}` cuando el archivo existe y `publish=true`.
  - NACK: `{"status":"NACK","filename":"nombre.ext"}` cuando no existe en la lista o no es publicable.

### Logs

- Consola y archivo `app.log` (en el directorio donde ejecutes `main.py`).
- Registra: nuevos archivos, eliminaciones, decisiones de publicación y guardados de configuración.

### Solución de problemas

- Timeout en el cliente UDP: asegúrate de que el servidor ya mostró "Servidor iniciado..." y sigue ejecutándose.
- Verificar que el puerto está abierto:
```bash
lsof -nP -iUDP:50000 | cat
```
- Ver logs recientes:
```bash
tail -n 50 app.log
```
- Ruta inválida: usa rutas ABSOLUTAS (p. ej., `/Users/tu_usuario/Downloads`).

### Detener el servidor

- Ctrl+C en la terminal donde corre el servidor, o:
```bash
pkill -f /Users/<TU_USUARIO>/Desktop/DNS/main.py
```



