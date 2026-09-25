from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent


def _env(name: str, default: str | None = None) -> str | None:
    return os.environ.get(name, default)


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _env_csv(name: str, default_csv: str = "") -> list[str]:
    raw = os.environ.get(name, default_csv)
    items = [x.strip() for x in raw.split(",") if x.strip()]
    return items


# --------------------------------------------------
# GENERAL
# --------------------------------------------------

SECRET_KEY = _env("DJANGO_SECRET_KEY", "change-me")
DEBUG = _env_bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = _env_csv(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1"
)


# --------------------------------------------------
# APPS
# --------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "corsheaders",

    "library",
    "auth_api",
]


# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "steamlike_backend.urls"


# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "steamlike_backend.wsgi.application"


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _env("POSTGRES_DB", "steamlike"),
        "USER": _env("POSTGRES_USER", "steamlike"),
        "PASSWORD": _env("POSTGRES_PASSWORD", "steamlike"),
        "HOST": _env("POSTGRES_HOST", "db"),
        "PORT": _env("POSTGRES_PORT", "5432"),
        "OPTIONS": {},
    }
}


# En Render PostgreSQL necesita SSL
if DATABASES["default"]["HOST"] != "db":
    DATABASES["default"]["OPTIONS"] = {
        "sslmode": "require",
    }


# --------------------------------------------------
# REDIS / CACHE
# --------------------------------------------------

# Prioridad:
# 1) REDIS_URL (Render)
# 2) REDIS_HOST + REDIS_PORT (Docker)
# 3) localhost (desarrollo sin Docker)

REDIS_URL = os.environ.get("REDIS_URL")

if not REDIS_URL:
    REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = os.environ.get("REDIS_PORT", "6379")

    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/1"

print("========== REDIS ==========")
print("ENV REDIS_URL =", os.environ.get("REDIS_URL"))
print("FINAL REDIS_URL =", REDIS_URL)
print("===========================")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}


# --------------------------------------------------
# PASSWORD VALIDATORS
# --------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]


# --------------------------------------------------
# LANGUAGE
# --------------------------------------------------

LANGUAGE_CODE = "es-es"

TIME_ZONE = "Europe/Madrid"

USE_I18N = True

USE_TZ = True


# --------------------------------------------------
# STATIC
# --------------------------------------------------

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --------------------------------------------------
# CORS + COOKIES
# --------------------------------------------------

CORS_ALLOWED_ORIGINS = _env_csv(
    "DJANGO_CORS_ALLOWED_ORIGINS",
    "http://frontend:3000,http://localhost:3000,http://localhost:5173"
)

CORS_ALLOW_CREDENTIALS = _env_bool(
    "DJANGO_CORS_ALLOW_CREDENTIALS",
    True
)

CSRF_TRUSTED_ORIGINS = _env_csv(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    "http://frontend:3000,http://localhost:3000,http://localhost:5173"
)

SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# --------------------------------------------------
# LOGGING
# --------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },

    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },

    "loggers": {
        "auth_api": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}