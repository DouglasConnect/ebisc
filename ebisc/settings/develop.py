from .base import *

DEBUG = True

IS_LIVE = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', '.charite.de', '*']

INTERNAL_IPS = ['127.0.0.1']

# -----------------------------------------------------------------------------
# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME', 'ebisc'),
        'USER': os.getenv('DB_USER', 'www'),
        'PASSWORD': os.getenv('DB_PASS'),
        'HOST': os.getenv('DB_HOST'),
    }
}

ELASTIC_INDEX = 'ebisc'
ELASTIC_HOSTS = [{'host': os.getenv('ES_HOST', 'localhost'), 'port': 9200}]

# -----------------------------------------------------------------------------
# Middleware class for API debugging

MIDDLEWARE_CLASSES += (
    'ebisc.middleware.NonHtmlDebugToolbarMiddleware',
)

# -----------------------------------------------------------------------------
