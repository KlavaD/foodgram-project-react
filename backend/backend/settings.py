import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = os.getenv(
    'SECRET_KEY',
    default='django-insecure-h9*6l$tj5k2f+gf10s&euquw5^3ky@&7007%0bwb)lic^@hy)u')

DEBUG = os.getenv('DEBUG', default=False)

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', default='*', ).split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'corsheaders',
    'django_filters',
    'users.apps.UserConfig',
    'recipes.apps.RecipesConfig',
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

# Database

BD_PROD = os.getenv('DB_PROD', default=False) == 'True'
if not BD_PROD:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': os.getenv(
                'DB_ENGINE', default='django.db.backends.postgresql'),
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT')
        }
    }

# Password validation

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

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 6,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}
DJOSER = {
    'USER_ID_FIELD': 'id',
    'LOGIN_FIELD': 'email',
    'PERMISSIONS': {
        'user_list': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
        'user': ['rest_framework.permissions.IsAuthenticated'],
    },
    'SERIALIZERS': {
        'user': 'users.serializers.CustomUserSerializer',
    },
    'HIDE_USERS': False,
}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Tomsk'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

FIELD_TEXT_LENGTH = 200

FIELD_EMAIL_LENGTH = 254

FIELD_COLOR_LENGTH = 7

NAMES_LENGTH = 150

AUTH_USER_MODEL = 'users.User'

INTERNAL_IPS = ['127.0.0.1', ]

CORS_URLS_REGEX = r'^/api/.*$'

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]

HEADERS = {
    'content-type': 'text/plain',
    'Content-Disposition': 'attachment; filename="shopping_cart.txt'
}

HEIGHT = 700

LEFT = 100
