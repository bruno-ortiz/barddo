from django.utils.importlib import import_module

LOADING_RECEIVERS = False


def receivers_autodiscover():
    """
    Auto-discover INSTALLED_APPS receivers.py modules and fail silently when
    not present. NOTE: receivers_autodiscover was inspired/copied from
    django.contrib.admin autodiscover
    """
    global LOADING_RECEIVERS
    if LOADING_RECEIVERS:
        return
    LOADING_RECEIVERS = True

    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:

        try:
            app_path = import_module(app).__path__
        except AttributeError:
            continue

        try:
            imp.find_module('receivers', app_path)
        except ImportError:
            continue

        import_module("%s.receivers" % app)

    LOADING_RECEIVERS = False