import os

fabconf = {}

#  Do not edit
fabconf['BASE_PATH'] = os.path.dirname(__file__)
fabconf['SERVER_USERNAME'] = "falleco"
fabconf['SSH_HOST'] = "barddo.com"
fabconf['SSH_PORT'] = 999

fabconf['PROJECT_PATH'] = ''
fabconf['APP_PATH'] = ''
fabconf['PYTHON_PATH'] = ''
fabconf['PIP_PATH'] = ''

fabconf['BRANCH'] = 'BARDDO-8' # TODO: change to default
fabconf['PROJECT_PATH.BETA'] = '/opt/barddo/source'
fabconf['APP_PATH.BETA'] = '/opt/barddo/source/barddo'
fabconf['PYTHON_PATH.BETA'] = '/opt/barddo/venv/bin/python'
fabconf['PIP_PATH.BETA'] = '/opt/barddo/venv/bin/pip'

# Full local path for .ssh
fabconf['SSH_PATH'] = "~/.ssh"

# Name of the private key file you use to connect to EC2 instances
fabconf['KEY_NAME'] = "barddo.pem"

# Don't edit. Full path of the ssh key you use to connect to EC2 instances
fabconf['SSH_PRIVATE_KEY_PATH'] = '%s/%s' % (fabconf['SSH_PATH'], fabconf['KEY_NAME'])