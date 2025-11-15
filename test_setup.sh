#!/bin/bash
# Script de prueba para el servidor de nombres de recursos de archivo

TEST_FOLDER="/Users/d4n911/Desktop/DNS_test"

echo "=========================================="
echo "Configuración de prueba"
echo "=========================================="
echo ""

# Crear carpeta de prueba si no existe
if [ ! -d "$TEST_FOLDER" ]; then
    echo "Creando carpeta de prueba: $TEST_FOLDER"
    mkdir -p "$TEST_FOLDER"
fi

# Crear archivos de prueba
echo "Creando archivos de prueba..."
echo "Contenido de prueba 1" > "$TEST_FOLDER/archivo1.txt"
echo "Contenido de prueba 2" > "$TEST_FOLDER/documento.pdf"
echo "Contenido de prueba 3" > "$TEST_FOLDER/imagen.jpg"
echo "Contenido de prueba 4" > "$TEST_FOLDER/script.py"

echo "✅ Archivos creados:"
ls -lh "$TEST_FOLDER"
echo ""
echo "Carpeta de prueba lista: $TEST_FOLDER"
echo ""
echo "Para iniciar el servidor, ejecuta:"
echo "  cd '/Users/d4n911/Desktop/DNS Dan/DNS'"
echo "  python3 main.py --folder '$TEST_FOLDER'"
echo ""
echo "En otra terminal, prueba con:"
echo "  python3 test_client.py archivo1 txt"
echo "  python3 test_client.py documento pdf"
echo "  python3 test_client.py imagen jpg"

