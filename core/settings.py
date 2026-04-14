
from pathlib import Path
import dj_database_url
import cloudinary
from dotenv import load_dotenv
import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.getenv("SECRET_KEY")


DEBUG = (os.getenv("DEBUG") or "").lower() == "true"


ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '')

ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS.split(',')] if ALLOWED_HOSTS else []

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', '')

CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in CSRF_TRUSTED_ORIGINS.split(',')] if CSRF_TRUSTED_ORIGINS else []
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # my apps
    'account',
    'base',
    'order',
    'crm',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'crm.context_processors.app_settings',
                'cart.context_processors.cart',

            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL')

        )
    }


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/
#
# STATIC_ROOT = str(BASE_DIR / 'staticfiles')
#
# STATIC_URL = '/static/'
#
# MEDIA_URL = '/media/'
#
# if DEBUG:
#     STATICFILES_DIRS = [str(BASE_DIR / 'static'), ]
# else:
#     STATIC_ROOT = str(BASE_DIR / 'static')
#
# MEDIA_ROOT = str(BASE_DIR / 'media')
#
#
#


STATIC_URL = '/static/'

# Where collectstatic will dump everything
STATIC_ROOT = str(BASE_DIR / 'staticfiles')

# Where your original static files live
STATICFILES_DIRS = [
    str(BASE_DIR / 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = str(BASE_DIR / 'media')




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = "account.User"


cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('API_SECRET'),
)


DOMAIN = os.getenv('DOMAIN')
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", None)
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", None)
ADMIN_PHONE_NUMBER = os.getenv("ADMIN_PHONE_NUMBER", None)


CART_SESSION_ID = 'cart'


DEFAULT_CACHE_TIMEOUT = 600

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PREFIX = os.getenv("REDIS_PREFIX", "dbt")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_HOST,
        "KEY_PREFIX": REDIS_PREFIX,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient", "CONNECTION_POOL_KWARGS": {}},
        "TIMEOUT": DEFAULT_CACHE_TIMEOUT,
    }
}

DEFAULT_PAGE_SIZE = os.getenv("DEFAULT_PAGE_SIZE", 10)

BROKER_URL = REDIS_HOST

CELERY_BROKER_URL = BROKER_URL
CELERY_RESULT_BACKEND = BROKER_URL
CELERY_BACKEND_URL = BROKER_URL
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_DEFAULT_QUEUE = REDIS_PREFIX
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True


FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL")