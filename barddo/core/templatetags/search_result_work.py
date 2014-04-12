from django.templatetags.i18n import register

__author__ = 'jovial'


@register.inclusion_tag('search_result/work.html')
def search_result_work(work):
    return {'work': work}