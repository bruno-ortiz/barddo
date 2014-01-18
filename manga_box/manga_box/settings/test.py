from base import *

########## IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

########## JENKINS TESTS CONFIGURATION
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INSTALLED_APPS += (
    'django_jenkins',
)

JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',   # select one django or
    #'django_jenkins.tasks.dir_tests'      # directory tests discovery
    #'django_jenkins.tasks.run_pep8',
    #'django_jenkins.tasks.run_pyflakes',
    #'django_jenkins.tasks.run_jslint',
    #'django_jenkins.tasks.run_csslint',
    #'django_jenkins.tasks.run_sloccount',
    #'django_jenkins.tasks.lettuce_tests',
)

PROJECT_APPS = LOCAL_APPS
########## END OF JENKINS TESTS CONFIGURATION