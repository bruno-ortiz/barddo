from django.templatetags.i18n import register

__author__ = 'jovial'


@register.inclusion_tag('work_element.html', takes_context=True)
def work_element(context, work, classes):
    return {'work': work, 'classes': classes, 'user': context['user']}