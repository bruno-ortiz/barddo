from django.templatetags.i18n import register

__author__ = 'jovial'


@register.inclusion_tag('person.html')
def person_result(person):
    """
    Custom tag to handle user result template
    """
    return {'person': person}