from django.templatetags.i18n import register

__author__ = 'jovial'


@register.inclusion_tag('search_result/person.html')
def search_result_person(person):
    return {'person': person}