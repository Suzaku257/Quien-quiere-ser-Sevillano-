"""
Aplicación principal de Quiz Educativo: ¿Quién Quiere Ser Sevillano?
Framework: Flask
Base de datos: MariaDB
Autor: Desarrollador Web Full-Stack
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import DatabaseManager
import os
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'tuClaveSecretaSuperSegura123!@#'  # Cambiar en producción

# Configuración de la sesión
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Inicializar gestor de base de datos (thread-safe con threading.local)
db = DatabaseManager(database='quiz_sevilla.db')

# Conectar a la base de datos al inicio
db.connect()


@app.before_request
def before_request():
    """Asegurar que la conexión de este thread esté disponible"""
    try:
        # threading.local() crea automáticamente una conexión para cada thread
        _ = db.connection
    except Exception as e:
        print(f"Error en before_request: {e}")


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Limpiar recursos al final de la petición"""
    # No desconectamos aquí - cada thread mantiene su conexión
    # SQLite/threading.local maneja esto automáticamente
    pass


# ============ RUTAS DE AUTENTICACIÓN ============

@app.route('/')
def index():
    """Página principal"""
    leaderboard = db.get_leaderboard()
    recent_scores = db.get_all_scores()[:10]
    return render_template(
        'index.html',
        leaderboard=leaderboard,
        recent_scores=recent_scores
    )


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Página y lógica de registro"""
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        # Validaciones
        errores = []
        
        if not nombre or len(nombre) < 3:
            errores.append('El nombre debe tener al menos 3 caracteres')
        
        if not email or '@' not in email:
            errores.append('Email inválido')
        
        if len(password) < 6:
            errores.append('La contraseña debe tener al menos 6 caracteres')
        
        if password != password_confirm:
            errores.append('Las contraseñas no coinciden')
        
        if errores:
            return render_template('registro.html', errores=errores)
        
        # Verificar si el email ya existe
        usuario_existente = db.get_user_by_email(email)
        if usuario_existente:
            return render_template('registro.html', errores=['El email ya está registrado'])
        
        # Registrar usuario
        success, result = db.register_user(nombre, email, password)
        if success:
            return render_template('registro_exitoso.html', email=email)
        else:
            return render_template('registro.html', errores=['Error al registrar usuario'])
    
    return render_template('registro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página y lógica de login"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            return render_template('login.html', error='Email y contraseña requeridos')
        
        # Buscar usuario
        usuarios = db.get_user_by_email(email)
        if not usuarios:
            return render_template('login.html', error='Email o contraseña incorrectos')
        
        usuario = usuarios[0]
        
        # Verificar contraseña
        if not db.verify_password(usuario['contraseña'], password):
            return render_template('login.html', error='Email o contraseña incorrectos')
        
        # Crear sesión
        session['user_id'] = usuario['id']
        session['nombre'] = usuario['nombre']
        session['email'] = usuario['email']
        
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    return redirect(url_for('index'))


# ============ RUTAS DEL QUIZ ============

@app.route('/dashboard')
def dashboard():
    """Panel de usuario"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    # Obtener estadísticas del usuario
    stats = db.get_user_stats(user_id)
    scores = db.get_user_scores(user_id)
    
    return render_template(
        'dashboard.html',
        nombre=session['nombre'],
        stats=stats,
        scores=scores
    )


@app.route('/quiz/start', methods=['GET', 'POST'])
def start_quiz():
    """Inicia el quiz"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Obtener 10 preguntas (aleatorias si hay más disponibles)
        preguntas = db.get_all_questions()
        if not preguntas:
            return render_template('quiz.html', error='No hay preguntas disponibles')

        total_quiz = 10
        if len(preguntas) > total_quiz:
            preguntas = random.sample(preguntas, total_quiz)
        else:
            preguntas = preguntas[:total_quiz]
        
        # Guardar preguntas en la sesión
        session['quiz_preguntas'] = [p['id'] for p in preguntas]
        session['quiz_respuestas'] = {}
        session['quiz_pregunta_actual'] = 0
        
        return redirect(url_for('quiz'))
    
    return render_template('start_quiz.html')


@app.route('/quiz')
def quiz():
    """Página del quiz"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if 'quiz_preguntas' not in session:
        return redirect(url_for('start_quiz'))
    
    pregunta_index = session.get('quiz_pregunta_actual', 0)
    preguntas_ids = session['quiz_preguntas']
    
    # Verificar si ya terminó el quiz
    if pregunta_index >= len(preguntas_ids):
        return redirect(url_for('result_quiz'))
    
    pregunta_id = preguntas_ids[pregunta_index]
    pregunta = db.get_question_by_id(pregunta_id)
    
    if not pregunta:
        return render_template('error.html', error='Pregunta no encontrada')
    
    return render_template(
        'quiz.html',
        pregunta=pregunta,
        numero_pregunta=pregunta_index + 1,
        total_preguntas=len(preguntas_ids)
    )


@app.route('/quiz/responder', methods=['POST'])
def responder():
    """Procesa la respuesta"""
    if 'user_id' not in session or 'quiz_preguntas' not in session:
        return redirect(url_for('login'))
    
    respuesta = request.form.get('respuesta')
    pregunta_index = session.get('quiz_pregunta_actual', 0)
    preguntas_ids = session['quiz_preguntas']
    
    if pregunta_index >= len(preguntas_ids):
        return redirect(url_for('result_quiz'))
    
    pregunta_id = preguntas_ids[pregunta_index]
    
    # Guardar respuesta en la sesión
    if 'quiz_respuestas' not in session:
        session['quiz_respuestas'] = {}
    
    session['quiz_respuestas'][str(pregunta_id)] = respuesta
    
    # Pasar a la siguiente pregunta
    session['quiz_pregunta_actual'] = pregunta_index + 1
    
    return redirect(url_for('quiz'))


@app.route('/quiz/resultado')
def result_quiz():
    """Muestra el resultado del quiz"""
    if 'user_id' not in session or 'quiz_preguntas' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    preguntas_ids = session['quiz_preguntas']
    respuestas = session.get('quiz_respuestas', {})
    
    # Calcular puntuación
    respuestas_correctas = 0
    total_preguntas = len(preguntas_ids)
    detalles = []
    
    for pregunta_id in preguntas_ids:
        pregunta = db.get_question_by_id(pregunta_id)
        respuesta_usuario = respuestas.get(str(pregunta_id), '')
        
        es_correcta = db.verify_answer(pregunta_id, respuesta_usuario)
        if es_correcta:
            respuestas_correctas += 1
        
        # Obtener las opciones como texto
        opciones_map = {
            'A': pregunta['opcion_a'],
            'B': pregunta['opcion_b'],
            'C': pregunta['opcion_c'],
            'D': pregunta['opcion_d']
        }
        
        detalles.append({
            'pregunta': pregunta['pregunta'],
            'respuesta_usuario': opciones_map.get(respuesta_usuario, 'No respondida'),
            'respuesta_correcta': opciones_map.get(pregunta['respuesta_correcta']),
            'correcta': es_correcta
        })
    
    # Calcular puntuación total
    puntuacion_total = int((respuestas_correctas / total_preguntas) * 100)
    
    # Guardar puntuación en la BD
    db.save_score(user_id, puntuacion_total, respuestas_correctas, total_preguntas)
    
    # Limpiar sesión del quiz
    session.pop('quiz_preguntas', None)
    session.pop('quiz_respuestas', None)
    session.pop('quiz_pregunta_actual', None)
    
    return render_template(
        'resultado.html',
        puntuacion_total=puntuacion_total,
        respuestas_correctas=respuestas_correctas,
        total_preguntas=total_preguntas,
        detalles=detalles
    )


# ============ RUTAS DE API ============

@app.route('/api/preguntas')
def api_preguntas():
    """Retorna todas las preguntas en JSON"""
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    preguntas = db.get_all_questions()
    return jsonify(preguntas)


@app.errorhandler(404)
def page_not_found(e):
    """Manejo de errores 404"""
    return render_template('error.html', error='Página no encontrada'), 404


@app.errorhandler(500)
def server_error(e):
    """Manejo de errores 500"""
    return render_template('error.html', error='Error interno del servidor'), 500


if __name__ == '__main__':
    # Conectar a BD al iniciar
    if db.connect():
        print("Conectado a la base de datos")
        app.run(debug=True, host='0.0.0.0', port=8000)
    else:
        print("No se pudo conectar a la base de datos")
