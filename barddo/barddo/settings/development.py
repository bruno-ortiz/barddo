"""Development settings and globals."""
from base import *

# ######### DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug

DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'barddo_development',
        'USER': 'barddo',
        'PASSWORD': 'barddo@01',
        'HOST': 'localhost',
        'PORT': '',
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

########## TOOLBAR CONFIGURATION
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INSTALLED_APPS += (
    'debug_toolbar',
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INTERNAL_IPS = ('127.0.0.1',)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TEMPLATE_CONTEXT': True,
}
########## END TOOLBAR CONFIGURATION


########## MISC CONFIGURATION
COMPRESS_OFFLINE = False

########## END OF MISC CONFIGURATION

##
#OAuth apps
##
SOCIAL_AUTH_FACEBOOK_KEY = '579142508831157'
SOCIAL_AUTH_FACEBOOK_SECRET = '3b9439528f2bd7cce28f25f8948f03fe'

SOCIAL_AUTH_GOOGLE_PLUS_KEY = '1010521892059-tf5leugg86ib3t2vsa2g4sbqm04lkj43.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_PLUS_SECRET = 'VWrV9x7s6Xxsr058StR6G09Q'

COMPRESS_ENABLED = True

##
#Paypal
##
PAYPAL_MODE = 'sandbox'
PAYPAL_CLIENT_ID = 'Af7rihD_C7HrZHSpkaTweMnq9ytxfRCaOwB1db2_LYcBWIu8V9UWsfnaveSW'
PAYPAL_CLIENT_SECRET = 'EPzfrRBZLH5FH7Dtvaakm0_PC-R4oNjBOplIocAyT9yLyN_S-wPla5qLSQkc'