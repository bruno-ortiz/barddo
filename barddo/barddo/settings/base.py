# -*- coding: utf-8 -*
from os import path
import sys
from os.path import dirname, abspath, basename


# ######### PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
sys.path.append(DJANGO_ROOT)
# ######### END PATH CONFIGURATION

# ######### DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
# ######### END DEBUG CONFIGURATION

# ######### MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Barddo', 'contact@barddo.com'),
)

DEFAULT_FROM_EMAIL = 'contact@barddo.com'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
# ######### END MANAGER CONFIGURATION

# ######### DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
# DATABASES = {
# 'default': {
# 'ENGINE': 'django.db.backends.postgresql_psycopg2',
# 'NAME': 'barddo_dev',
# 'USER': 'postgres',
# 'PASSWORD': 'postgres',
# 'HOST': 'localhost',
# 'PORT': '5432',
# }
# }
# ######### END DATABASE CONFIGURATION

# ######### GENERAL CONFIGURATION
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('pt', 'Português'),
    ('en', 'English'),
)

LOCALE_PATHS = (
    path.normpath(path.join(SITE_ROOT, 'locale')),
)

SITE_ID = 1

DATE_INPUT_FORMATS = ('%d-%m-%Y',)

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
# ######### END GENERAL CONFIGURATION

# ######### MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = path.normpath(path.join(SITE_ROOT, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# Documents folder
DOCUMENTS_ROOT = path.normpath(path.join(SITE_ROOT, 'documents'))
########## END MEDIA CONFIGURATION

########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = path.normpath(path.join(SITE_ROOT, 'static'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    path.normpath(path.join(SITE_ROOT, 'assets')),
    path.normpath(path.join(SITE_ROOT, 'feedback', 'assets')),
    path.normpath(path.join(SITE_ROOT, 'search', 'assets')),
    path.normpath(path.join(SITE_ROOT, 'core', 'assets')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
    'dajaxice.finders.DajaxiceFinder',
    'shards.finders.ShardsFinder',
)
########## END STATIC FILE CONFIGURATION

########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
#SECRET_KEY = r"{{ secret_key }}"
SECRET_KEY = 'hzwh&w(=(@tib_jt71&v4ypfw&#7dln^=2a^i7(y3nyvuqe%(_'
########## END SECRET CONFIGURATION

########## SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []
########## END SITE CONFIGURATION

########## FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    path.normpath(path.join(SITE_ROOT, 'core', 'fixtures')),
    path.normpath(path.join(SITE_ROOT, 'publishing', 'fixtures')),
    path.normpath(path.join(SITE_ROOT, 'accounts', 'fixtures')),
    path.normpath(path.join(SITE_ROOT, 'payments', 'fixtures')),
)
########## END FIXTURE CONFIGURATION

########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'django.core.context_processors.csrf',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    path.normpath(path.join(SITE_ROOT, 'templates')),
    path.normpath(path.join(SITE_ROOT, 'core', 'templates')),
    path.normpath(path.join(SITE_ROOT, 'feedback', 'templates')),
    path.normpath(path.join(SITE_ROOT, 'shards', 'templates')),
    path.normpath(path.join(SITE_ROOT, 'publishing', 'templates')),
    path.normpath(path.join(SITE_ROOT, 'accounts', 'templates')),
    path.normpath(path.join(SITE_ROOT, 'payments', 'templates')),
)
########## END TEMPLATE CONFIGURATION

########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'accounts.middleware.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'barddo.middleware.XsSharing'
)
########## END MIDDLEWARE CONFIGURATION

########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % SITE_NAME
########## END URL CONFIGURATION

########## APP CONFIGURATION
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.formtools',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin panel and documentation:
    #'django_admin_bootstrapped',
    'django.contrib.admin',
)

THIRD_PARTY_APPS = (
    'south',
    'django_extensions',
    'compressor',

    'dajaxice',
    'dajax',

    'widget_tweaks',
    'social.apps.django_app.default',
    'endless_pagination',
    'imagekit',
    'easy_thumbnails',
    'analytical',
    'polymorphic',
    'django_bitly',
    'redis_metrics',
    'djcelery',
    'rest_framework',
    'rest_framework.authtoken',
    'paypalrestsdk',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'shards',
    'core',
    'accounts',
    'feedback',
    'publishing',
    'rating',
    'search',
    'follow',
    'payments',
    'feed',
    'share',
    'api',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
########## END APP CONFIGURATION

########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },

        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': '/tmp/barddo.log',
            'maxBytes': 1024000,
            'backupCount': 3,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },

        'dajaxice': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
########## END LOGGING CONFIGURATION

########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME
########## END WSGI CONFIGURATION

########## SCSS COMPRESSOR CONFIGURATION
COMPRESS_PARSER = 'compressor.parser.LxmlParser'
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
#COMPRESS_MTIME_DELAY = 20
COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/less', 'lessc {infile} > {outfile}'),
    ('text/x-sass', 'sass --compass {infile} {outfile}'),
    ('text/x-scss', 'scss --compass {infile} {outfile}'),
)

COMPRESS_ROOT = STATIC_ROOT
########## END OF SCSS COMPRESSOR CONFIGURATION

##
#SOCIAL AUTH CONFIG
##
AUTHENTICATION_BACKENDS = (
    'accounts.models.BarddoUserAuthBackend',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GooglePlusAuth',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_USER_MODEL = 'accounts.BarddoUser'

SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL

SOCIAL_AUTH_DEFAULT_USERNAME = 'Barddo'
SOCIAL_AUTH_UID_LENGTH = 32
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 32
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 32
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 32

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.user_details',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'accounts.pipelines.create_user_profile',
    'accounts.pipelines.get_avatar',
    'accounts.pipelines.get_birth_date',
    'accounts.pipelines.get_gender',
    'accounts.pipelines.get_country',
    'accounts.pipelines.get_language',
    'accounts.pipelines.post_user_creation',
)

SOCIAL_AUTH_LOGIN_URL = '/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error'  # TODO: handle that

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_about_me', 'user_birthday', 'user_location']

########## Image crop settings
THUMBNAIL_ALIASES = {
    '': {
        'big_cover': {'size': (261, 300), 'crop': False},
        'small_cover': {'size': (163, 236), 'crop': False},
    },
    'core.WorkPage.image': {
        'reader_thumbs': {'size': (136, 136), 'crop': True},
    },
}

########## End of image crop settings

########## Analytics Services Settigns
# Disabled tracking ips
ANALYTICAL_INTERNAL_IPS = ['0.0.0.0', '127.0.0.1', 'localhost']

# Do the best to identify users on tracking tools that can handle this
ANALYTICAL_AUTO_IDENTIFY = True

# Url: http://clicky.com/
# Description: A real time analytics site
# Type: free tier
CLICKY_SITE_ID = '100737229'

# Url: https://www.crazyegg.com
# Description: A PAID heat map, we are on trial, started ad 17/05/2014 and ends at 17/06/2014
# Type: Paid Yearly
CRAZY_EGG_ACCOUNT_NUMBER = '00230100'

# Url: https://www.google.com/analytics
# Description: Google Analytics Services
# Type: free tier
GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-50511116-2'
GOOGLE_ANALYTICS_SITE_SPEED = True

# Url: https://www.woopra.com
# Description: Another real time analytics, but better at showing what the user is doing
# Type: trial
#WOOPRA_DOMAIN = 'barddo.com'
########## End of analytics Services Settigns

LOGIN_URL = "/"
LOGOUT_URL = "/logout"

#### Bitly Settings

BITLY_LOGIN = "icrisanto"

BITLY_API_KEY = "R_c5a307706efef2c2881a88a748120435"

#### End of Bitly Settings

#### Metrics Settings

REDIS_METRICS_HOST = 'localhost'
REDIS_METRICS_PORT = 6379
REDIS_METRICS_DB = 0
REDIS_METRICS_PASSWORD = None
REDIS_METRICS_SOCKET_TIMEOUT = None
REDIS_METRICS_SOCKET_CONNECTION_POOL = None

### End of Metrics Settings


#### Celery Settings
BROKER_URL = 'amqp://guest:guest@localhost//'  # unsecure, for now
#### End of Celery Settings

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),

    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],

    'PAGINATE_BY': 25
}