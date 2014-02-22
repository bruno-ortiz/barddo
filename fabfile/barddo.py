from fabric.api import sudo, env, run, task, cd
from fabric.colors import green as _green
from fabric.operations import require
from config import *
import time


env.user = fabconf['SERVER_USERNAME']
env.port = fabconf['SSH_PORT']
env.key_filename = fabconf['SSH_PRIVATE_KEY_PATH']
env.host_string = fabconf['SSH_HOST']

@task
def main():
    # TODO
    env.service = ""
    env.settings = ""
    env.project = fabconf['PROJECT_PATH']
    env.app = fabconf['APP_PATH']
    env.python = fabconf['PYTHON_PATH']
    env.pip = fabconf['PIP_PATH']
    env.branch = fabconf['BRANCH']

@task
def beta():
    env.service = "barddo"
    env.settings = "barddo.settings.production"
    env.project = fabconf['PROJECT_PATH.BETA']
    env.app = fabconf['APP_PATH.BETA']
    env.python = fabconf['PYTHON_PATH.BETA']
    env.pip = fabconf['PIP_PATH.BETA']
    env.branch = fabconf['BRANCH']

@task
def full_deploy():
    """
    Restart the server applying new migrations
    """
    require("service")
    start_time = time.time()
    print(_green("Starting deploy..."))

    stop_services()
    update_repository()
    update_pip()
    cleanup()
    apply_static()
    apply_compress()
    apply_migrations()
    start_services()

    end_time = time.time()
    print(_green("Runtime: %f minutes" % ((end_time - start_time) / 60)))
    print(_green(env.host_string))


def stop_services():
    print(_green("Stopping Supervidor..."))
    sudo("supervisorctl stop " + env.service)


def start_services():
    print(_green("Starting Supervidor..."))
    sudo("supervisorctl start " + env.service)


def update_repository():
    print(_green("Updating repository"))
    with cd(env.app):
        run('hg pull')
        run('hg up -C ' + env.branch)
        run('hg purge')


def update_pip():
    print(_green("Updating pip requirements"))
    with cd(env.project):
        run(env.pip + ' install -r requirements.pip')


def cleanup():
    print(_green("Cleanup *.pyc files"))
    with cd(env.app):
        run('find . -name *.pyc | xargs rm -f')


def apply_static():
    print(_green("Collecting static files"))
    with cd(env.app):
        sudo(env.python + ' manage.py collectstatic --noinput --settings=' + env.settings, user=env.user)


def apply_compress():
    print(_green("Compressing static files"))
    with cd(env.app):
        sudo(env.python + ' manage.py compress --settings=' + env.settings, user=env.user)


def apply_migrations():
    print(_green("Applying migrations"))
    with cd(env.app):
        sudo(env.python + ' manage.py migrate --all --settings=' + env.settings, user=env.user)