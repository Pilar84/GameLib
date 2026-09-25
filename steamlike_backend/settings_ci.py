from .settings import *

# Base de datos para GitHub Actions (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
    }
}

# Desactivar DEBUG en CI
DEBUG = False
