import os
from pathlib import Path
import environ

from pathlib import Path
from .celery import app as celery_app

__all__ = ("celery_app",)
# 1. Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Initialize env with defaults
env = environ.Env(
    DEBUG=(bool, False)
)

# 3. Read the .env file once using the absolute path
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# 4. Assign variables
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
# This line tells Django to look specifically for the .env file in the BASE_DIR
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()  # reads .env


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # If you want a global templates folder in your root, add it here:
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True, # THIS MUST BE TRUE
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
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "http://127.0.0.1:8000"])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "portfolio",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DATABASES = {
    "default": env.db(default="sqlite:///db.sqlite3")
}

# Celery settings
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://redis:6379/0")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="redis://redis:6379/0")


ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'
