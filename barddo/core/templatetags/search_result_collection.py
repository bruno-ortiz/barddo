from django.templatetags.i18n import register

__author__ = 'jovial'


@register.inclusion_tag('search_result/collection.html')
def search_result_collection(collection):
    return {'collection': collection}