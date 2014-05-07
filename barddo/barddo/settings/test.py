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
    #'django_jenkins',
)

JENKINS_TASKS = (
    #'django_jenkins.tasks.with_coverage',
    #'django_jenkins.tasks.django_tests',   # select one django or
    #'django_jenkins.tasks.dir_tests'      # directory tests discovery
    #'django_jenkins.tasks.run_pep8',
    #'django_jenkins.tasks.run_pyflakes',
    #'django_jenkins.tasks.run_jslint',
    #'django_jenkins.tasks.run_csslint',
    #'django_jenkins.tasks.run_sloccount',
    #'django_jenkins.tasks.lettuce_tests',
)

FIXTURE_DIRS += (path.normpath(path.join(SITE_ROOT, 'accounts', 'test-fixtures')),
                 path.normpath(path.join(SITE_ROOT, 'publishing', 'test-fixtures')))

PROJECT_APPS = LOCAL_APPS
########## END OF JENKINS TESTS CONFIGURATION

DEBUG = False

########## MISC CONFIGURATION
COMPRESS_OFFLINE = False


##
# Disable SOUTH
##
SOUTH_TESTS_MIGRATE = False
SKIP_SOUTH_TESTS = True