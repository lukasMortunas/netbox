import os

#########################
#                       #
#   Required settings  Indeed #
#                       #
#########################

# ALLOWED_HOSTS - read from env var set in Azure App Service
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', 'localhost').split(',')]

# PostgreSQL database configuration - read from environment variables
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', ''),
        'CONN_MAX_AGE': 300,
    }
}

# Redis database settings - read from environment variables
REDIS = {
    'tasks': {
        'HOST': os.getenv('REDIS_HOST'),
        'PORT': int(os.getenv('REDIS_PORT', 6380)),
        'PASSWORD': os.getenv('REDIS_PASSWORD'),
        'DATABASE': 0,
        'SSL': os.getenv('REDIS_SCHEME', 'redis').startswith('rediss'),
    },
    'caching': {
        'HOST': os.getenv('REDIS_HOST'),
        'PORT': int(os.getenv('REDIS_PORT', 6380)),
        'PASSWORD': os.getenv('REDIS_PASSWORD'),
        'DATABASE': 1,
        'SSL': os.getenv('REDIS_SCHEME', 'redis').startswith('rediss'),
    }
}

# SECRET_KEY - read from environment variable
SECRET_KEY = os.getenv('SECRET_KEY')

# API_TOKEN_PEPPERS - read from environment variable
API_TOKEN_PEPPERS = {
    1: os.getenv('API_TOKEN_PEPPER_1'),
}


#########################
#                       #
#   Optional settings   #
#                       #
#########################

ADMINS = []

AUTH_PASSWORD_VALIDATORS = []

BASE_PATH = ''

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = []
CORS_ORIGIN_REGEX_WHITELIST = []

CSRF_COOKIE_NAME = 'csrftoken'

# DEBUG should be False in production
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

DEFAULT_LANGUAGE = 'en-us'

# Email settings - optional, read from environment if needed
EMAIL = {
    'SERVER': os.getenv('EMAIL_SERVER', 'localhost'),
    'PORT': int(os.getenv('EMAIL_PORT', 25)),
    'USERNAME': os.getenv('EMAIL_USERNAME', ''),
    'PASSWORD': os.getenv('EMAIL_PASSWORD', ''),
    'USE_SSL': os.getenv('EMAIL_USE_SSL', 'False').lower() == 'true',
    'USE_TLS': os.getenv('EMAIL_USE_TLS', 'False').lower() == 'true',
    'TIMEOUT': 10,
    'FROM_EMAIL': os.getenv('EMAIL_FROM', ''),
}

EXEMPT_VIEW_PERMISSIONS = []
