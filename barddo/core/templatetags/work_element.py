from django.templatetags.i18n import register

__author__ = 'jovial'


@register.inclusion_tag('work_element.html')
def work_element(work, classes):
    return {'work': work, 'classes': classes}