"""
Django settings for crm project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import environ
import datetime
from urllib.parse import urlparse


SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(SRC_DIR)
PROJECT_DIR = os.path.join(SRC_DIR, 'crm')


env = environ.Env()
env_file = os.path.join(SRC_DIR, '.env')
if os.path.exists(env_file):
    env.read_env(env_file)

SECRET_KEY = env('SECRET_KEY', default='ratxf8^p-$9@w@%u+_q6jfa!d+7(t%f!=m^tj*6w-dz@4mr(cs')

DEBUG = env.bool('DEBUG', default=True)
APP_MODE = env.str('APP_MODE', default='production')

IS_PRODUCTION = APP_MODE == 'production'

BASE_FRONT_URL = env('BASE_FRONT_URL').rstrip('/')
ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'channels',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'files',
    'payment',

    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'markdownx',
    'adminsortable2',

    'sorl.thumbnail',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'rest_auth',
    'rest_auth.registration',

    'corsheaders',

    'users.apps.UsersConfig',
    'courses_access.apps.CoursesAccessConfig',
    'courses',
    'search',
    'constants',
    'providers',

    'dialogs',
    'reports',
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

ROOT_URLCONF = 'crm.urls'

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

WSGI_APPLICATION = 'crm.wsgi.application'
ASGI_APPLICATION = 'crm.asgi.application'


DATABASES = {
    'default': env.db(),
}


REDIS_URL = os.environ.get('REDIS_URL')
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(urlparse(REDIS_URL).hostname, urlparse(REDIS_URL).port)],
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MARKDOWNX_MEDIA_PATH = 'uploads/lessons/{}'.format(datetime.datetime.now().strftime('%Y/%m/'))
MARKDOWNX_SERVER_CALL_LATENCY = 120000  # 2min
MARKDOWNX_MARKDOWN_EXTENSIONS = [
    'pymdownx.magiclink',
    'pymdownx.highlight',
    'pymdownx.extra',
    'fenced_code',
    'md_in_html',
    'admonition',
    'legacy_attrs',
    'legacy_em',
    'meta',
    'nl2br',
    'sane_lists',
    'smarty',
    'toc',
    'wikilinks',
]


AUTHENTICATION_BACKENDS = (
    'users.auth_backend.SuperPasswordBackend',
)

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True

SITE_ID = 1

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
DEFAULT_ADMIN_EMAIL = env('DEFAULT_ADMIN_EMAIL')

MAILGUN_TOKEN = env('MAILGUN_TOKEN')
MAILGUN_HOST = env('MAILGUN_HOST')

AUTH_USER_MODEL = 'users.User'


REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'users.serializers.UserDetailSerializer',
    'PASSWORD_RESET_SERIALIZER': 'users.serializers.PasswordResetSerializer',
    'PASSWORD_CHANGE_SERIALIZER': 'users.serializers.PasswordChangeSerializer',
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'users.serializers.RegisterSerializer',
}

REST_USE_JWT = True
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'users.auth.UserNameEmailJSONWebTokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_ALLOW_REFRESH': True,
}

CELERY_BROKER_URL = REDIS_URL
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60


SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
      'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
      }
   }
}


SENTRY_DSN = env('SENTRY_DSN', default=None)
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        send_default_pii=True
    )


TINKOFF_URL = env('TINKOFF_URL')
TINKOFF_TERMINAL_KEY = env('TINKOFF_TERMINAL_KEY')
TINKOFF_TERMINAL_PASSWORD = env('TINKOFF_TERMINAL_PASSWORD')

TINKOFF_CREDIT_URL = env('TINKOFF_CREDIT_URL')
TINKOFF_CREDIT_SHOP_ID = env('TINKOFF_CREDIT_SHOP_ID')
TINKOFF_CREDIT_SHOWCASE_ID = env('TINKOFF_CREDIT_SHOWCASE_ID')
