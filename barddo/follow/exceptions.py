from django.db import IntegrityError

__author__ = 'bruno'


class AlreadyExistsError(IntegrityError):
    pass