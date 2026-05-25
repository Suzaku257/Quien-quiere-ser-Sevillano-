#!/usr/bin/env python3
import sys
import os
os.chdir('/home/alumnado/Escritorio/curso')
sys.path.insert(0, '/home/alumnado/Escritorio/curso')

from app import app, db

if __name__ == '__main__':
    if db.connect():
        print("✓ Conectado a la base de datos")
        print("✓ Aplicación iniciando en http://0.0.0.0:8000")
        app.run(debug=True, host='0.0.0.0', port=8000, use_reloader=False)
    else:
        print("✗ No se pudo conectar a la BD")
        sys.exit(1)
