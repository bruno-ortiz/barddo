import logging

from django import template
from django.middleware.csrf import get_token
from django.conf import settings
from django.core.files.storage import get_storage_class

from shards.core import shards_config


staticfiles_storage = get_storage_class(settings.STATICFILES_STORAGE)()
register = template.Library()
log = logging.getLogger('shards')


@register.simple_tag(takes_context=True)
def shards_js_import(context, csrf=True):
    """ Return the js script tag for the shards.js file
    If the csrf argument is present and it's ``nocsrf`` shards will not
    try to mark the request as if it need the csrf token. By default use
    the shards_js_import template tag will make django set the csrftoken
    cookie on the current request."""

    csrf = csrf != 'nocsrf'
    request = context.get('request')

    if request and csrf:
        get_token(request)
    elif csrf:
        if not shards_config.SHARDS_IGNORE_REQUEST_NOT_IN_CONTEXT:
            log.warning("The 'request' object must be accessible within context.")

    url = staticfiles_storage.url('shards/shards.js')
    return '<script src="%s" type="text/javascript" charset="utf-8"></script>' % url