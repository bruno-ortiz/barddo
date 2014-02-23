from shards.core import shards_core


def register_shard(*args, **kwargs):
    """
    Decorator used to register views that act can return a template shard
    """

    # When no argument provided
    if len(args) and not kwargs:
        callable = args[0]
        shards_core.register(callable)
        return callable

    # When argument provided, we must wrap on another decorator
    def decorator(callable):
        shards_core.register(callable, *args, **kwargs)
        return callable

    return decorator
