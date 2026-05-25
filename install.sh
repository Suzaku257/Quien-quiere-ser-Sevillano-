#!/bin/bash

# Script de instalación rápida para ¿Quién Quiere Ser Sevillano?

echo "======================================"
echo "¿Quién Quiere Ser Sevillano?"
echo "Quiz Educativo sobre Sevilla"
echo "======================================"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    echo "Por favor, instala Python 3.8 o superior"
    exit 1
fi

echo "✓ Python 3 detectado: $(python3 --version)"
echo ""

# Crear entorno virtual
echo "[1/4] Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

echo "✓ Entorno virtual creado"
echo ""

# Instalar dependencias
echo "[2/4] Instalando dependencias..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error al instalar dependencias"
    exit 1
fi

echo "✓ Dependencias instaladas"
echo ""

# Verificar MariaDB
echo "[3/4] Validando conexión a MariaDB..."
python3 -c "
import mysql.connector
try:
    conn = mysql.connector.connect(host='localhost', user='root', password='')
    if conn.is_connected():
        print('✓ MariaDB conectado correctamente')
    conn.close()
except Exception as e:
    print('⚠️  No se pudo conectar a MariaDB')
    print('Asegúrate de que MariaDB esté ejecutándose')
"
echo ""

# Setup de BD
echo "[4/4] Configurando base de datos..."
python3 setup_db.py

if [ $? -ne 0 ]; then
    echo "❌ Error al configurar la base de datos"
    exit 1
fi

echo ""
echo "======================================"
echo "✓ ¡Instalación completada!"
echo "======================================"
echo ""
echo "Para iniciar la aplicación, ejecuta:"
echo "  source venv/bin/activate"
echo "  python3 app.py"
echo ""
echo "La aplicación estará en: http://localhost:5000"
echo ""
