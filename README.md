# ¿Quién Quiere Ser Sevillano? - Quiz Educativo

Una aplicación web completa y educativa desarrollada en Python con Flask para aprender sobre la historia, cultura, monumentos y tradiciones de Sevilla.

## 🎯 Características

- **Quiz Interactivo**: 20+ preguntas sobre Sevilla con 4 opciones de respuesta
- **Sistema de Autenticación**: Registro seguro con hashing de contraseñas
- **Gestión de Puntuaciones**: Almacenamiento de histórico de intentos
- **Dashboard Personal**: Visualización de estadísticas y progreso
- **Interfaz Responsiva**: Diseño adaptable a dispositivos móviles
- **Base de Datos**: MariaDB para persistencia de datos

## 📋 Requisitos Técnicos

- Python 3.8+
- MariaDB 10.5+
- pip (gestor de paquetes de Python)

## 🚀 Instalación Rápida

### 1. Clonar el repositorio

```bash
cd /path/to/proyecto
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar la base de datos

Asegúrate de que MariaDB esté ejecutándose. Si necesitas credenciales diferentes, edita `setup_db.py`:

```bash
python setup_db.py
```

Este comando:
- Crea la base de datos `quiz_sevilla`
- Crea las tablas necesarias (usuarios, preguntas, puntuaciones)
- Puebla la BD con 20 preguntas sobre Sevilla

### 4. Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en: **http://localhost:5000**

## 📁 Estructura del Proyecto

```
curso/
├── app.py                 # Aplicación principal Flask
├── database.py            # Gestión de base de datos
├── setup_db.py            # Script de setup de BD
├── requirements.txt       # Dependencias del proyecto
├── static/
│   └── style.css          # Estilos CSS globales
└── templates/
    ├── base.html          # Template base
    ├── index.html         # Página principal
    ├── registro.html      # Formulario de registro
    ├── login.html         # Formulario de login
    ├── dashboard.html     # Panel del usuario
    ├── start_quiz.html    # Pantalla de inicio del quiz
    ├── quiz.html          # Interfaz del quiz
    ├── resultado.html     # Resultados del quiz
    └── error.html         # Página de errores
```

## 🗂️ Estructura de Base de Datos

### Tabla: usuarios
- `id` (INT, PK, AUTO_INCREMENT)
- `nombre` (VARCHAR 100)
- `email` (VARCHAR 100, UNIQUE)
- `contraseña` (VARCHAR 64, SHA256)
- `fecha_registro` (DATETIME)
- `activo` (BOOLEAN)

### Tabla: preguntas
- `id` (INT, PK, AUTO_INCREMENT)
- `pregunta` (TEXT)
- `opcion_a`, `opcion_b`, `opcion_c`, `opcion_d` (VARCHAR 255)
- `respuesta_correcta` (CHAR 1: A, B, C, D)
- `categoria` (VARCHAR 50)
- `dificultad` (ENUM: facil, media, dificil)

### Tabla: puntuaciones
- `id` (INT, PK, AUTO_INCREMENT)
- `usuario_id` (INT, FK)
- `puntuacion_total` (INT: 0-100)
- `respuestas_correctas` (INT)
- `respuestas_totales` (INT)
- `fecha_intento` (DATETIME)

## 🔐 Seguridad

- **Hashing de Contraseñas**: Utiliza SHA256 para almacenar contraseñas de forma segura
- **Validación de Entrada**: Todas las entradas se validan en servidor
- **Sesiones Seguras**: Uso de sesiones Flask con secret key

## 📝 Uso de la Aplicación

### 1. Registro
- Acceder a la página de inicio
- Hacer clic en "Registrarse"
- Completar formulario con nombre, email y contraseña
- Validaciones automáticas de campos

### 2. Login
- Introducir email y contraseña
- Acceso al dashboard personal

### 3. Dashboard
- Ver estadísticas personales (mejores puntuaciones, promedio, etc.)
- Visualizar historial de intentos
- Opción para comenzar nuevo quiz

### 4. Quiz
- Responder 20 preguntas sobre Sevilla
- Navegación fácil entre preguntas
- Barra de progreso visual
- Información sobre categorías

### 5. Resultados
- Puntuación final y porcentaje
- Detalles de cada respuesta
- Comparación con respuesta correcta
- Opción para repetir el quiz

## 🎓 Categorías de Preguntas

- 🏛️ **Monumentos**: Preguntas sobre la arquitectura y sitios históricos
- 📜 **Historia**: Hechos históricos sobre Sevilla
- 🗺️ **Geografía**: Ubicación, barrios, ríos
- 🎭 **Cultura**: Arte, música, tradiciones
- 🎉 **Tradiciones**: Fiestas, costumbres sevillanas

## 🔧 Configuración

### Cambiar credenciales de BD

En `database.py`, línea 17-20:
```python
db = DatabaseManager(
    host='localhost',
    user='root',
    password='tu_contraseña',
    database='quiz_sevilla'
)
```

### Cambiar puerto de Flask

En `app.py`, línea final:
```python
app.run(debug=True, host='localhost', port=5000)
```

## 📊 Mejoras Futuras

- [ ] Sistema de rankings entre usuarios
- [ ] Diferentes dificultades de preguntas
- [ ] Certificados al completar quiz
- [ ] Sistema de logros y badges
- [ ] Comentarios explicativos para cada pregunta
- [ ] Exportar resultados en PDF
- [ ] Integración con redes sociales

## 🐛 Solución de Problemas

### Error: "No se puede conectar a la BD"
```
Verificar que MariaDB esté ejecutándose
Verificar credenciales en database.py
Verificar que la BD existe: ejecutar setup_db.py
```

### Error: "Módulo no encontrado"
```
pip install -r requirements.txt
```

### Puerto 5000 en uso
```
python app.py # Cambiar puerto en el código
```

## 📜 Licencia

Este proyecto es de código abierto y está disponible bajo licencia MIT.

## 👨‍💻 Autor

Desarrollador Web Full-Stack especializado en Python
Año: 2026

## 📧 Soporte

Para reportar bugs o sugerencias, contactar al equipo de desarrollo.

---

**¡Disfruta aprendiendo sobre la hermosa ciudad de Sevilla!** 🌟
