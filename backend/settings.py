import os
from pathlib import Path
from pymongo import MongoClient

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 Clave secreta desde variable de entorno (con fallback)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'clave-insegura-por-defecto')

# 🐛 Debug según entorno
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# 🌐 Dominios permitidos
ALLOWED_HOSTS = ['backend-react-jvqo.onrender.com', 'localhost']

# 🧩 Apps instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',  # CORS para peticiones externas
]

# ⚙️ Middlewares
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # servir estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 🌍 CORS
CORS_ALLOW_ALL_ORIGINS = True  # ⚠️ Solo para pruebas (permite solicitudes desde file://, Netlify, etc.)

# 🧠 URL y WSGI
ROOT_URLCONF = 'backend.urls'
WSGI_APPLICATION = 'backend.wsgi.application'

# 🧱 Base de datos predeterminada (no usada, pero obligatoria)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🔡 Plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 🗓️ Config regional
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# 📁 Archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = []
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 🔐 Validación de contraseñas (opcional)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 🔗 MongoDB Atlas
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["react"]
users_collection = db["users"]
