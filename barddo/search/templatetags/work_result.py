from django.templatetags.i18n import register

__author__ = 'jovial'


@register.inclusion_tag('work.html')
def work_result(work):
    return {'work': work}