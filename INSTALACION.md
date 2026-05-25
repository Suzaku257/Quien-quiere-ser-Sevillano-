# 📦 Guía de Instalación - ¿Quién Quiere Ser Sevillano?

## 🖥️ Requisitos del Sistema

### Windows
- Python 3.8 o superior
- MariaDB 10.5 o MySQL 5.7+
- Mínimo 2GB RAM
- 500MB de espacio disponible

### Linux (Ubuntu/Debian)
- Python 3.8 o superior
- MariaDB 10.5 o MySQL 5.7+
- Mínimo 2GB RAM
- 500MB de espacio disponible

### macOS
- Python 3.8 o superior
- MariaDB 10.5 o MySQL 5.7+
- Mínimo 2GB RAM
- 500MB de espacio disponible

---

## 📋 Paso a Paso: Instalación Completa

### 1️⃣ Instalar Python

#### Windows
```
1. Descarga desde: https://www.python.org/downloads/
2. Ejecuta el instalador
3. ✓ Marca "Add Python to PATH"
4. Click en "Install Now"
```

Verifica la instalación:
```cmd
python --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version
```

#### macOS
```bash
# Usando Homebrew
brew install python3
python3 --version
```

---

### 2️⃣ Instalar y Configurar MariaDB

#### Windows
```
1. Descargar: https://mariadb.org/download/
2. Ejecutar el instalador
3. Durante la instalación:
   - Usa puerto: 3306 (default)
   - Usuario: root
   - Contraseña: (dejar vacío o usar una)
4. Completa la instalación
```

Verifica que está ejecutándose:
```cmd
mysql --version
```

#### Linux (Ubuntu/Debian)
```bash
# Instalar MariaDB
sudo apt install mariadb-server

# Verificar que está corriendo
sudo service mysql status

# Si no está corriendo
sudo service mysql start
```

#### macOS
```bash
# Usando Homebrew
brew install mariadb

# Iniciar MariaDB
mysql.server start
```

---

### 3️⃣ Descargar el Proyecto

```bash
# Navega a donde quieras descargar el proyecto
cd C:\Users\TuUsuario\Documentos  # Windows
cd ~/Documentos                     # Linux/Mac

# Clona o descarga el proyecto
# (Copiar la carpeta 'curso' a este directorio)
```

---

### 4️⃣ Instalar Dependencias Python

```bash
# Navega a la carpeta del proyecto
cd curso

# Windows
pip install -r requirements.txt

# Linux/Mac
pip3 install -r requirements.txt
```

Verifica que se instaló correctamente:
```bash
pip list
```

Deberías ver:
```
Flask                    3.0.0
flask-session            0.5.0
mysql-connector-python   8.2.0
werkzeug                 3.0.1
python-dotenv            1.0.0
```

---

### 5️⃣ Configurar la Base de Datos

#### Verificar conexión a MariaDB

```bash
# Windows
mysql -u root

# Linux/Mac
mysql -u root
```

Si conecta, saldrá:
```
mysql>
```

Escribe `exit` para salir.

#### Si da error, verifica que MariaDB esté ejecutándose

**Windows:**
```cmd
# Abre Services (servicios)
# Busca MariaDB
# Click derecho → Start
```

**Linux:**
```bash
sudo service mysql start
```

**macOS:**
```bash
mysql.server start
```

---

### 6️⃣ Crear Base de Datos

Ejecuta el script de setup:

```bash
# Windows
python setup_db.py

# Linux/Mac
python3 setup_db.py
```

Deberías ver:

```
=== SETUP BASE DE DATOS QUIZ SEVILLA ===

[1/3] Creando base de datos...
✓ Base de datos creada
[2/3] Creando tablas...
✓ Tabla usuarios creada
✓ Tabla preguntas creada
✓ Tabla puntuaciones creada
[3/3] Poblando preguntas...
✓ 20 preguntas insertadas

✓ Setup completado exitosamente
Puede ejecutar: python app.py
```

---

### 7️⃣ Ejecutar la Aplicación

```bash
# Windows
python app.py

# Linux/Mac
python3 app.py
```

Verás:

```
✓ Conectado a la base de datos
 * Running on http://localhost:5000
 * Restarting with reloader
 * Debugger is active!
 * Debugger PIN: xxx-xxx-xxx
```

---

### 8️⃣ Abrir en el Navegador

Abre tu navegador favorito y ve a:

```
http://localhost:5000
```

¡La aplicación debería estar en funcionamiento! 🎉

---

## 🆘 Solución de Problemas

### Problema: "No reconoce el comando python"

**Windows:**
```
1. Click derecho en Este PC → Propiedades
2. Avanzadas → Variables de entorno
3. Path → Nueva entrada: C:\Users\TuUsuario\AppData\Local\Programs\Python\Python310
4. Reinicia la terminal
```

**Linux:**
```bash
# Usa python3 en lugar de python
python3 --version
python3 setup_db.py
```

### Problema: "No se puede conectar a MariaDB"

**Verificar que está corriendo:**

Windows:
```cmd
# Abre Services (servicios) y busca MySQL o MariaDB
# Debe estar en estado "Running"
```

Linux:
```bash
sudo service mysql status
sudo service mysql start
```

macOS:
```bash
mysql.server status
mysql.server start
```

### Problema: "Módulo flask no encontrado"

```bash
# Reinstala dependencias
pip install --upgrade -r requirements.txt

# O instala manualmente
pip install flask flask-session mysql-connector-python
```

### Problema: "Puerto 5000 ya en uso"

Edita `app.py`, última línea:

```python
# Cambiar de:
app.run(debug=True, host='localhost', port=5000)

# A:
app.run(debug=True, host='localhost', port=5001)  # O cualquier otro puerto
```

### Problema: "Error al crear la base de datos"

Verifica que el usuario MySQL tiene permisos:

```bash
mysql -u root
mysql> SHOW DATABASES;
mysql> exit
```

Si falla, intenta con `sudo`:

```bash
sudo python3 setup_db.py
```

---

## 🚀 Alternativas de Instalación

### Usando Entorno Virtual (Recomendado)

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python app.py
```

### Script de Instalación Automática

Si usas Linux/Mac:

```bash
chmod +x install.sh
./install.sh
```

---

## ✅ Verificación Final

Cuando hayas completado la instalación, verifica:

1. **Python instalado**: `python --version`
2. **MariaDB corriendo**: Intenta conectar con `mysql -u root`
3. **Dependencias**: `pip list` debe mostrar Flask y otros
4. **Base de datos**: `mysql -u root quiz_sevilla -e "SELECT COUNT(*) FROM preguntas;"`
5. **Aplicación**: `http://localhost:5000` abre en navegador

---

## 🎓 Primeros Pasos en la App

1. **Registrarse**: Clic en "Registrarse" en página principal
2. **Completar formulario**: Nombre, email, contraseña
3. **Login**: Con tus credenciales
4. **Comenzar Quiz**: Desde el Dashboard
5. **Responder preguntas**: Selecciona A, B, C o D
6. **Ver resultados**: Puntuación y retroalimentación

---

## 📞 Soporte

Si encuentras problemas:

1. Revisa la sección "Solución de Problemas"
2. Verifica los requisitos del sistema
3. Consulta README.md para más información
4. Revisa QUICKSTART.md para uso rápido

---

## 📝 Notas Importantes

- La aplicación está optimizada para navegadores modernos (Chrome, Firefox, Safari, Edge)
- Requiere conexión de red local (localhost)
- Los datos se guardan en MariaDB automáticamente
- Puedes reiniciar la app sin perder datos
- El script setup_db.py es seguro ejecutar múltiples veces

---

**¡Felicidades! Aplicación instalada y lista para usar.** 🎉

Para comenzar, abre: **http://localhost:5000**
