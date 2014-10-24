import os

fabconf = {}

#  Do not edit
fabconf['BASE_PATH'] = os.path.dirname(__file__)
fabconf['SERVER_USERNAME'] = "mangas"
fabconf['SSH_HOST'] = "mangasbrasil.com"
fabconf['SSH_PORT'] = 999

fabconf['BRANCH'] = 'feature/BARDDO-120'
fabconf['PROJECT_PATH'] = '/opt/mangasbrasil/sources'
fabconf['APP_PATH'] = '/opt/mangasbrasil/sources/barddo'
fabconf['PYTHON_PATH'] = '/opt/mangasbrasil/venv/bin/python'
fabconf['PIP_PATH'] = '/opt/mangasbrasil/venv/bin/pip'

# Full local path for .ssh
fabconf['SSH_PATH'] = "~/.ssh"

# Name of the private key file you use to connect to EC2 instances
fabconf['KEY_NAME'] = "mangasbrasil.pem"

# Don't edit. Full path of the ssh key you use to connect to EC2 instances
fabconf['SSH_PRIVATE_KEY_PATH'] = '%s/%s' % (fabconf['SSH_PATH'], fabconf['KEY_NAME'])