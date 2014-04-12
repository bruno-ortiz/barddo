from django.templatetags.i18n import register

__author__ = 'jovial'


@register.inclusion_tag('person.html')
def person_result(person):
    return {'person': person}