from django.conf import settings

from manager import Shards


class ShardsConfig(object):
    """
    Provide an easy to use way to read the shards configuration and
    return the default values if no configuration is present.
    """

    default_config = {
        'SHARDS_EXCEPTION': 'SHARDS_EXCEPTION',
        'SHARDS_MEDIA_PREFIX': 'shards',
        'SHARDS_NOT_CALLABLE_RESPONSE': '{"error":"400 Bad Request"}',
        'SHARDS_IGNORE_REQUEST_NOT_IN_CONTEXT': False
    }

    def __getattr__(self, name):
        """
        Return the customized value for a setting (if it exists) or the
        default value if not.
        """

        if name in self.default_config:
            if hasattr(settings, name):
                return getattr(settings, name)
            return self.default_config.get(name)
        return None

    @property
    def shards_url(self):
        return r'^%s/' % self.SHARDS_MEDIA_PREFIX

    @property
    def django_settings(self):
        return settings

    @property
    def modules(self):
        return shards_core.modules


shards_config = ShardsConfig()
shards_core = Shards()
