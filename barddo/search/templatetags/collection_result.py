from django.templatetags.i18n import register

__author__ = 'jovial'


@register.inclusion_tag('collection.html')
def collection_result(collection):
    """
    Custom tag to handle collection result template
    """
    return {'collection': collection}