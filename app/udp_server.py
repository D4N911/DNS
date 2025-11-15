import json
import logging
import os
import socket
from typing import Tuple

from .config import ConfigManager


log = logging.getLogger(__name__)


class UdpServer:
    def __init__(self, config: ConfigManager, host: str = "0.0.0.0", port: int = 50000) -> None:
        self._config = config
        self._host = host
        self._port = port

    def _handle_request(self, data: bytes, addr: Tuple[str, int]) -> bytes:
        try:
            payload = json.loads(data.decode("utf-8"))
            # Acepta tanto formato nuevo (nombre y extensión separados) como formato antiguo (filename completo)
            filename = payload.get("filename")
            extension = payload.get("extension", "")
            
            # Si no viene extensión, intentar extraer del filename o buscar por filename completo
            if filename and not extension:
                base, ext = os.path.splitext(filename)
                if ext:
                    filename = base
                    extension = ext.lstrip(".")
                else:
                    # Formato antiguo: buscar por nombre completo
                    meta = self._config.get_file(payload.get("filename"))
                    if meta and meta.publish:
                        resp = {"status": "ACK", "filename": meta.filename, "extension": meta.extension, "ttl": meta.ttl}
                    else:
                        resp = {"status": "NACK", "filename": payload.get("filename"), "extension": ""}
                    return json.dumps(resp).encode("utf-8")
            
            if not filename or not isinstance(filename, str):
                return json.dumps({"status": "NACK", "error": "invalid filename"}).encode("utf-8")
            
            # Buscar por nombre y extensión separados
            meta = self._config.get_file_by_name_and_ext(filename, extension or "")
            if meta and meta.publish:
                resp = {"status": "ACK", "filename": meta.filename, "extension": meta.extension, "ttl": meta.ttl}
            else:
                resp = {"status": "NACK", "filename": filename, "extension": extension or ""}
            return json.dumps(resp).encode("utf-8")
        except Exception as e:
            log.warning(f"Solicitud inválida desde {addr}: {e}")
            return json.dumps({"status": "NACK", "error": "bad request"}).encode("utf-8")

    def run(self) -> None:
        log.info(f"Servidor UDP escuchando en {self._host}:{self._port}")
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((self._host, self._port))
            while True:
                data, addr = sock.recvfrom(8192)
                resp = self._handle_request(data, addr)
                sock.sendto(resp, addr)


