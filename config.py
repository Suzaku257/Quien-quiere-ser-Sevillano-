"""
Configuración de la aplicación
Cambiar según sea necesario para el entorno
"""

import os
from datetime import timedelta

# ===== CONFIGURACIÓN DE BD =====
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'quiz_sevilla'),
    'port': int(os.environ.get('DB_PORT', 3306))
}

# ===== CONFIGURACIÓN DE FLASK =====
class Config:
    """Configuración base"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-123')
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_PERMANENT = False
    
    # Configuración de depuración
    DEBUG = os.environ.get('FLASK_DEBUG', True)
    TESTING = False

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    DEVELOPMENT = True

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    DEVELOPMENT = False
    # Cambiar SECRET_KEY en producción
    SECRET_KEY = os.environ.get('SECRET_KEY', 'YOU_MUST_CHANGE_THIS_IN_PRODUCTION')

# ===== CATEGORÍAS DE PREGUNTAS =====
CATEGORIAS = [
    'monumentos',
    'historia',
    'geografía',
    'cultura',
    'tradiciones'
]

# ===== CONFIGURACIÓN DEL QUIZ =====
QUIZ_CONFIG = {
    'total_preguntas': 20,
    'tiempo_par_respuesta': None,  # Sin límite de tiempo
    'puntos_por_respuesta_correcta': 5,
    'mostrar_explicacion': True
}

# ===== VALIDACIONES DE FORMULARIO =====
VALIDATION = {
    'nombre_min_length': 3,
    'nombre_max_length': 100,
    'password_min_length': 6,
    'email_regex': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
}
