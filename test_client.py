#!/usr/bin/env python3
"""
Cliente de prueba para el servidor UDP de nombres de recursos de archivo.
Permite probar las consultas ACK/NACK.
"""

import json
import socket
import sys
import time


def test_udp_query(host: str = "127.0.0.1", port: int = 50000, filename: str = "", extension: str = ""):
    """Envía una consulta UDP y muestra la respuesta."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        
        # Formato nuevo: nombre y extensión separados
        if filename and extension:
            payload = {"filename": filename, "extension": extension}
        elif filename:
            # Si solo viene filename, intentar extraer extensión
            import os
            base, ext = os.path.splitext(filename)
            if ext:
                payload = {"filename": base, "extension": ext.lstrip(".")}
            else:
                payload = {"filename": filename}
        else:
            print("Error: Debes especificar filename y extension, o al menos filename")
            return False
        
        print(f"Enviando consulta: {json.dumps(payload)}")
        sock.sendto(json.dumps(payload).encode("utf-8"), (host, port))
        
        data, addr = sock.recvfrom(4096)
        response = json.loads(data.decode("utf-8"))
        
        print(f"Respuesta recibida: {json.dumps(response, indent=2)}")
        
        if response.get("status") == "ACK":
            print(f"✅ ACK: Archivo disponible (TTL: {response.get('ttl')}s)")
            return True
        else:
            print(f"❌ NACK: Archivo no disponible")
            return False
            
    except socket.timeout:
        print("❌ Timeout: El servidor no respondió en 5 segundos")
        print("   Asegúrate de que el servidor esté ejecutándose en el puerto 50000")
        return False
    except ConnectionRefusedError:
        print("❌ Error: Conexión rechazada")
        print("   Asegúrate de que el servidor esté ejecutándose en el puerto 50000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        sock.close()


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 test_client.py <filename> [extension]")
        print("Ejemplos:")
        print("  python3 test_client.py archivo txt")
        print("  python3 test_client.py documento pdf")
        print("  python3 test_client.py archivo.txt  # formato legacy")
        sys.exit(1)
    
    filename = sys.argv[1]
    extension = sys.argv[2] if len(sys.argv) > 2 else ""
    
    print("=" * 50)
    print("Cliente de prueba - Servidor UDP de nombres de recursos")
    print("=" * 50)
    print()
    
    test_udp_query(filename=filename, extension=extension)


if __name__ == "__main__":
    main()

