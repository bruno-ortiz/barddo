from shards.core import shards_core


def register_shard(*args, **kwargs):
    """
    Decorator used to register views that act can return a template shard
    """

    # When no argument provided
    if len(args) and not kwargs:
        _callable = args[0]
        shards_core.register(_callable)
        return _callable

    # When argument provided, we must wrap on another decorator
    def decorator(_func):
        shards_core.register(_func, *args, **kwargs)
        return _func

    return decorator
