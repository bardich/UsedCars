from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

INSTALLED_APPS += [
    'django_extensions',
    # 'debug_toolbar',  # Disabled for clean UI
]

# MIDDLEWARE += [
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# ]

# INTERNAL_IPS = ['127.0.0.1']

# Database - use SQLite by default for development, PostgreSQL via env vars
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DB_NAME', BASE_DIR / 'db.sqlite3'),
    }
}

# Add PostgreSQL credentials only if using PostgreSQL
if 'postgresql' in DATABASES['default']['ENGINE']:
    DATABASES['default'].update({
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    })

# Disable password validation in development
AUTH_PASSWORD_VALIDATORS = []

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Tailwind CSS - NPM path configuration
# Using Node.js installed inside virtual environment
NPM_BIN_PATH = os.path.join(BASE_DIR, 'venv', 'bin', 'npm')

# Simple console logging for development
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
