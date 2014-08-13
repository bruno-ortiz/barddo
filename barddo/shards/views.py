import logging

from django.conf import settings
from django.views.generic.base import View
from django.http import HttpResponse, Http404

from shards.core import shards_core, shards_config

log = logging.getLogger('shards')


def safe_dict(d):
    """
    Recursively clone json structure with UTF-8 dictionary keys
    http://www.gossamer-threads.com/lists/python/bugs/684379
    """
    if isinstance(d, dict):
        return dict([(k.encode('utf-8'), safe_dict(v)) for k, v in d.iteritems()])
    elif isinstance(d, list):
        return [safe_dict(x) for x in d]
    else:
        return d


class ShardRequest(View):
    """
    Handle all the shards requests
    """

    def dispatch(self, request, name=None, **kwargs):

        if not name:
            raise Http404

        # Check if the function is callable
        if shards_core.is_callable(name):

            callable = shards_core.get(name)

            try:
                request_method = getattr(request, request.method)
                data = request_method.dict()
            except Exception:
                data = {}

            # Call the function. If something goes wrong, handle the Exception
            try:
                response = callable.call(request, **data)
            except Exception as ex:
                log.exception('name=%s, data=%s, error=%s', name, data, ex)

                if settings.DEBUG:
                    raise

                response = shards_config.SHARDS_EXCEPTION

            return HttpResponse(response, content_type="application/json; charset=utf-8")
        else:
            log.error('Function %s is not callable. method=%s', name, request.method)
            return HttpResponse(shards_config.SHARDS_NOT_CALLABLE_RESPONSE,
                                content_type="application/json; charset=utf-8")