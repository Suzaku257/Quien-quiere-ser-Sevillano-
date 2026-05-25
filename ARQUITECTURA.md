# 🏗️ Arquitectura Técnica - ¿Quién Quiere Ser Sevillano?

## Descripción General

"¿Quién Quiere Ser Sevillano?" es una aplicación web full-stack desarrollada en **Python** con **Flask** y **MariaDB**, que permite a los usuarios participar en un quiz educativo interactivo sobre Sevilla.

## 🎯 Stack Tecnológico

### Backend
- **Framework**: Flask 3.0.0
- **Lenguaje**: Python 3.8+
- **Base de Datos**: MariaDB 10.5+
- **Gestor de Sesiones**: Flask-Session
- **Seguridad**: SHA256 para hashing de contraseñas

### Frontend
- **HTML5**: Markup semántico
- **CSS3**: Diseño responsivo con Flexbox y CSS Grid
- **JavaScript**: Interactividad (opcional)
- **Responsive**: Mobile-first design

### Dependencias
```
Flask==3.0.0
flask-session==0.5.0
mysql-connector-python==8.2.0
werkzeug==3.0.1
python-dotenv==1.0.0
```

## 📊 Arquitectura de Datos

### Diagrama Entidad-Relación

```
┌─────────────────┐
│    USUARIOS     │
├─────────────────┤
│ id (PK)         │
│ nombre          │
│ email (UNIQUE)  │
│ contraseña      │
│ fecha_registro  │
│ activo          │
└────────┬────────┘
         │1
         │
         │ N
         │
┌────────▼──────────────┐
│  PUNTUACIONES         │
├──────────────────────┤
│ id (PK)              │
│ usuario_id (FK)      │
│ puntuacion_total     │
│ respuestas_correctas │
│ respuestas_totales   │
│ fecha_intento        │
└──────────────────────┘


┌──────────────────┐
│    PREGUNTAS     │
├──────────────────┤
│ id (PK)          │
│ pregunta         │
│ opcion_a         │
│ opcion_b         │
│ opcion_c         │
│ opcion_d         │
│ respuesta_correcta
│ categoria        │
│ dificultad       │
└──────────────────┘
```

## 🔄 Flujo de Datos

### 1. Registro de Usuario
```
[Formulario] → [Validación HTML] → [Verificación Backend] → 
[Hash Contraseña] → [INSERT BD] → [Confirmación]
```

### 2. Login
```
[Credenciales] → [Búsqueda en BD] → [Verificación Hash] → 
[Crear Sesión] → [Redirect Dashboard]
```

### 3. Quiz Workflow
```
[Iniciar Quiz] → [Cargar Preguntas] → [Mostrar Pregunta] → 
[Responder] → [Validar] → [Siguiente] → [Calcular Score] → 
[Guardar en BD] → [Mostrar Resultado]
```

## 🗂️ Estructura de Directorios

```
curso/
│
├── app.py                    # Aplicación principal Flask
│   ├── Rutas de autenticación
│   ├── Rutas del quiz
│   ├── Rutas de API
│   └── Manejo de errores
│
├── database.py              # Gestor de base de datos
│   ├── Conexión a MariaDB
│   ├── Operaciones CRUD
│   ├── Hash de contraseñas
│   └── Validación de respuestas
│
├── setup_db.py              # Script de inicialización
│   ├── Creación de BD
│   ├── Creación de tablas
│   └── Población de datos
│
├── config.py                # Configuración
│   └── Variables de entorno
│
├── requirements.txt         # Dependencias Python
│
├── static/                  # Archivos estáticos
│   └── style.css           # Estilos CSS globales
│
├── templates/              # Templates HTML (Jinja2)
│   ├── base.html           # Template base
│   ├── index.html          # Página principal
│   ├── registro.html       # Formulario registro
│   ├── login.html          # Formulario login
│   ├── dashboard.html      # Panel usuario
│   ├── start_quiz.html     # Inicio del quiz
│   ├── quiz.html           # Pantalla del quiz
│   ├── resultado.html      # Resultados
│   └── error.html          # Página de error
│
├── README.md               # Documentación completa
├── QUICKSTART.md           # Guía de inicio rápido
└── .env.example            # Ejemplo de configuración


```

## 🔐 Seguridad

### Contraseñas
- **Algoritmo**: SHA256
- **Almacenamiento**: Hasheada en BD
- **Validación**: Mínimo 6 caracteres

### Sesiones
- **Tipo**: Filesystem sessions
- **Duración**: 24 horas
- **Secret Key**: Configurada en Flask

### Validación de Entrada
- Validación HTML5 en cliente
- Validación Python en servidor
- Sanitización de datos de BD

## 📈 Flujos de Usuario

### Nuevo Usuario
```
1. Accede a http://localhost:5000
2. Hace clic en "Registrarse"
3. Completa formulario con validaciones
4. Contraseña se hashea y almacena
5. Recibe confirmación
6. Puede hacer login
```

### Usuario Existente
```
1. Login con email y contraseña
2. Contraseña se verifica contra hash
3. Se crea sesión de usuario
4. Acceso a Dashboard
5. Visualiza estadísticas
6. Puede comenzar quiz
```

### Durante el Quiz
```
1. Se cargan 20 preguntas de BD
2. Se guardan IDs en sesión
3. Se muestra una pregunta a la vez
4. Usuario selecciona opción
5. Se valida la respuesta
6. Progresa a la siguiente
7. Al terminar, calcula score
8. Guarda en BD tabla puntuaciones
9. Muestra resultados detallados
```

## 🎨 Interfaz de Usuario

### Componentes principales

**Navbar**
- Logo/Marca
- Información usuario (cuando autenticado)
- Botón Cerrar Sesión

**Formularios**
- Con validación en cliente y servidor
- Mensajes de error claros
- Campos requeridos indicados

**Quiz**
- Barra de progreso
- Opciones de respuesta con radio buttons
- Sidebar con categoría actual
- Botones Siguiente/Finalizar

**Dashboard**
- Cards de estadísticas
- Tabla de histórico
- Botón para comenzar quiz

**Resultados**
- Círculo con puntuación grande
- Mensaje personalizado según score
- Detalle pregunta por pregunta
- Botones para repetir o volver

## 📊 Estadísticas Disponibles

Para cada usuario se calcula:
- **Total de intentos**: COUNT(*)
- **Puntuación máxima**: MAX(puntuacion_total)
- **Puntuación promedio**: AVG(puntuacion_total)
- **Total respuestas correctas**: SUM(respuestas_correctas)

## 🔌 API REST (Opcional)

La aplicación incluye endpoints básicos:

```
GET /api/preguntas
  - Retorna todas las preguntas en JSON
  - Requiere autenticación
  - Response: Array de objetos pregunta
```

## 🚀 Optimizaciones

### Rendimiento
- Conexión reutilizable a BD
- Queries optimizadas con índices
- Session se mantiene abierta

### UX
- Diseño responsivo
- Progreso visual clara
- Mensajes de confirmación
- Validación instantánea

## 🧪 Testing

### Escenarios de prueba

1. **Registro**
   - Email válido/inválido
   - Contraseñas coincidentes/no-coincidentes
   - Nombres muy cortos/largos

2. **Login**
   - Credenciales correctas/incorrectas
   - Email no registrado
   - Contraseña incorrecta

3. **Quiz**
   - Navegar preguntas
   - Cambiar respuestas
   - Completar quiz
   - Ver resultados

4. **Base de Datos**
   - Creación tablas
   - Inserción de datos
   - Recuperación de información
   - Integridad referencial

## 📝 Logs y Debugging

En desarrollo, la aplicación imprime:
- Conexión/Desconexión BD
- Errores de consultas
- Fases del quiz

## 🌐 Deployment

Para producción, considerar:
- Usar gunicorn en lugar de Flask dev server
- Configurar HTTPS/SSL
- Usar base de datos remota
- Establecer SECRET_KEY fuerte
- DEBUG = False
- Usar variables de entorno

## 📚 Referencias

- [Flask Documentation](https://flask.palletsprojects.com/)
- [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/)
- [MariaDB Documentation](https://mariadb.com/kb/en/)

---

**Fecha de creación**: 25 de Mayo de 2026
**Versión**: 1.0.0
**Estado**: Producción Ready ✓
