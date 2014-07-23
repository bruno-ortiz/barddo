"""Production settings and globals."""
from os import environ

from base import *

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured


def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)

# ######### HOST CONFIGURATION
# See: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = ['.barddo.com', 'barddo.com', '127.0.0.1:8000']
# ######### END HOST CONFIGURATION


# ######### EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = environ.get('EMAIL_HOST', 'email-smtp.us-east-1.amazonaws.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', 'ApndY0q7AeWJZBQSop07FbJVwF2gW8n5PE6IUVt7PYTn')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', 'AKIAIEAC5JJOJSQDSQVA')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = environ.get('EMAIL_PORT', 587)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = EMAIL_HOST_USER
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'barddo_production',  # Or path to database file if using sqlite3.
        'USER': 'barddo',
        'PASSWORD': 'barddo@01',
        'HOST': 'datanode.israelcrisanto.com',
        'PORT': '',  # Set to empty string for default.
    }
}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION

########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
#SECRET_KEY = get_env_setting('SECRET_KEY')
########## END SECRET CONFIGURATION

INSTALLED_APPS += (
    'gunicorn',
)

DEBUG = False

TEMPLATE_DEBUG = DEBUG

##
#OAuth apps
##
FACEBOOK_APP_NAME = 'barddo'
SOCIAL_AUTH_FACEBOOK_KEY = '1375067126097037'
SOCIAL_AUTH_FACEBOOK_SECRET = '1be5226a3b8fa841b35e178baf026b01'

SOCIAL_AUTH_GOOGLE_PLUS_KEY = '1010521892059-25jnl53uid47dpoqj7ljdqh9m4sanvvg.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_PLUS_SECRET = 'YCWhljOVuudcJhg59ws26M1j'

REDIS_METRICS_HOST = 'datanode.israelcrisanto.com'
REDIS_METRICS_PORT = 6379
REDIS_METRICS_DB = 0
REDIS_METRICS_PASSWORD = "batatinha_quando_nasce_espalha_a_rama_pelo_chao"
REDIS_METRICS_SOCKET_TIMEOUT = None
REDIS_METRICS_SOCKET_CONNECTION_POOL = None

##
#Paypal
##
PAYPAL_MODE = 'live'
PAYPAL_CLIENT_ID = 'Aa6cixDo7JJG5m4QAqy3VINZA6orEcCE2JfAzmJrMCfvhIHxVC1dDABRlAM5'
PAYPAL_CLIENT_SECRET = 'EG2JiBD08TCzAyOnQgW_loVIu_BtiQIM9dtVge7G3vhtv6DpkAyTeq7uSgUA'

##
# Cross Site API
##
XS_SHARING_ALLOWED_ORIGINS = '*'
XS_SHARING_ALLOWED_METHODS = "POST, GET"
XS_SHARING_ALLOWED_HEADERS = "Authorization"