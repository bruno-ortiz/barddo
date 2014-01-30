__author__ = 'bruno'

from django.template import Library

register = Library()


@register.filter
def is_false(var):
    return var is False