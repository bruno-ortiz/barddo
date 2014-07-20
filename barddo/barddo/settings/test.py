from base import *

########## IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "barddo.db",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

########## JENKINS TESTS CONFIGURATION
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INSTALLED_APPS += (
    'django_jenkins',
)

FIXTURE_DIRS += (path.normpath(path.join(SITE_ROOT, 'accounts', 'test-fixtures')),
                 path.normpath(path.join(SITE_ROOT, 'publishing', 'test-fixtures')))

PROJECT_APPS = LOCAL_APPS
########## END OF JENKINS TESTS CONFIGURATION

DEBUG = False

########## MISC CONFIGURATION
COMPRESS_OFFLINE = False

##
#OAuth apps
##
SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''
SOCIAL_AUTH_GOOGLE_PLUS_KEY = ''
SOCIAL_AUTH_GOOGLE_PLUS_SECRET = ''

##
# Disable SOUTH
##
SOUTH_TESTS_MIGRATE = False
SKIP_SOUTH_TESTS = True

XS_SHARING_ALLOWED_ORIGINS = '*'
XS_SHARING_ALLOWED_METHODS = "POST, GET, OPTIONS, PUT, DELETE"
XS_SHARING_ALLOWED_HEADERS = "Authorization"