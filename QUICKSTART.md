# 📚 Guía de Inicio Rápido - ¿Quién Quiere Ser Sevillano?

## 🚀 Inicio en 5 Minutos

### Paso 1: Prerequisitos
Asegúrate de tener instalados:
- Python 3.8+
- MariaDB o MySQL ejecutándose

### Paso 2: Descargar archivos
```bash
# Navega a la carpeta del proyecto
cd /ruta/del/proyecto
```

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Base de Datos
```bash
python setup_db.py
```

Verás:
```
✓ Base de datos creada
✓ Tabla usuarios creada
✓ Tabla preguntas creada
✓ Tabla puntuaciones creada
✓ 20 preguntas insertadas
✓ Setup completado exitosamente
```

### Paso 5: Ejecutar la aplicación
```bash
python app.py
```

Verás:
```
✓ Conectado a la base de datos
* Running on http://localhost:5000
```

### Paso 6: Abrir en navegador
Abre: **http://localhost:5000**

---

## 🔐 Crear Primer Usuario

1. Haz clic en **"Registrarse"**
2. Completa el formulario:
   - Nombre: Tu nombre
   - Email: tu@email.com
   - Contraseña: Mínimo 6 caracteres
3. Haz clic en **"Registrarse"**
4. Verás confirmación y podrás hacer login

---

## 🎮 Juegar el Quiz

1. Login con tus credenciales
2. En el Dashboard, haz clic en **"Comenzar Quiz"**
3. Lee cada pregunta cuidadosamente
4. Selecciona la respuesta correcta (A, B, C o D)
5. Haz clic en **"Siguiente Pregunta"** o **"Finalizar Quiz"**
6. Visualiza tu puntuación y respuestas

---

## 📊 Ver Estadísticas

En el Dashboard puedes ver:
- **Intentos Realizados**: Total de veces que has jugado
- **Puntuación Máxima**: Tu mejor resultado
- **Puntuación Promedio**: Media de tus puntuaciones
- **Respuestas Correctas**: Total de respuestas acertadas
- **Historial**: Tabla con detalles de cada intento

---

## 🐛 Solución de Problemas Comunes

### Problema: "No se puede conectar a MariaDB"
**Solución:**
```bash
# En Linux/Mac
sudo service mysql start

# En Windows
net start MySQL80
# o abre MySQL Workbench
```

### Problema: "Error al insertar preguntas"
**Solución:**
```bash
# Verifica que la base de datos exista
mysql -u root -p
mysql> SHOW DATABASES;
mysql> USE quiz_sevilla;
mysql> SELECT COUNT(*) FROM preguntas;
```

### Problema: "Error 'Secret Key'"
**Solución:**
- Es solo una advertencia en desarrollo
- Se solucionará automáticamente en producción

### Problema: "Puerto 5000 ya en uso"
**Solución:**
Edita la última línea de `app.py`:
```python
app.run(debug=True, host='localhost', port=5001)  # Cambia a otro puerto
```

---

## 📝 Preguntas Incluidas

El quiz includes 20 preguntas sobre:

1. Capital de España (Geografía)
2. Exposición Iberoamericana (Historia)
3. Monumento emblemático (Monumentos)
4. Río que atraviesa Sevilla (Geografía)
5. Naves de la Catedral (Monumentos)
6. Ubicación Alcázar (Monumentos)
7. Festividades (Tradiciones)
8. Diseño Torre del Oro (Historia)
9. Altura de la Giralda (Monumentos)
10. Arte de azulejos (Cultura)
... y 10 preguntas más

---

## 💾 Archivos Importantes

| Archivo | Descripción |
|---------|------------|
| `app.py` | Aplicación principal Flask |
| `database.py` | Gestión de base de datos |
| `setup_db.py` | Script de inicialización |
| `requirements.txt` | Dependencias Python |
| `templates/` | Archivos HTML |
| `static/style.css` | Estilos CSS |

---

## 🔧 Personalización

### Agregar más preguntas
Edita `setup_db.py`:
```python
PREGUNTAS_SEVILLA = [
    {
        'pregunta': '¿Tu pregunta aquí?',
        'opcion_a': 'Opción A',
        'opcion_b': 'Opción B',
        'opcion_c': 'Opción C',
        'opcion_d': 'Opción D',
        'respuesta_correcta': 'B',  # Letra correcta
        'categoria': 'historia'
    },
    # ... más preguntas
]
```

Luego:
```bash
python setup_db.py
```

### Cambiar colores de la aplicación
Edita `static/style.css`, línea 14-21:
```css
:root {
    --color-primary: #d4af37;      /* Color dorado */
    --color-secondary: #f0f0f0;    /* Color secundario */
    --color-dark: #333;             /* Color oscuro */
    /* ... más colores */
}
```

---

## 📱 Acceso Móvil

La aplicación funciona perfectamente en:
- ✓ Teléfonos Android/iOS
- ✓ Tablets
- ✓ Computadoras de escritorio

Simplemente accede a:
```
http://localhost:5000
```
desde cualquier dispositivo en la misma red.

---

## ⚡ Rendimiento

- **Carga inicial**: < 1 segundo
- **Quiz completo**: ~5-10 minutos
- **Respuesta del servidor**: < 200ms

---

## 📞 Soporte Técnico

Si encuentras problemas:

1. Verifica los logs en la terminal
2. Consulta la sección de "Solución de Problemas"
3. Revisa que todas las dependencias estén instaladas

---

**¡Bienvenido a ¿Quién Quiere Ser Sevillano!** 🌟

Disfruta aprendiendo sobre la hermosa ciudad de Sevilla mientras compites por la mejor puntuación.
