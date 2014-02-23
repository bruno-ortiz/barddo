import inspect
import logging

from django.views.generic import View

from shards.exceptions import InvalidClassViewError


log = logging.getLogger('shards')


class Shards(object):
    def __init__(self):
        """
        Shard manager, receiver callables available and knows how to find them
        """
        self._callables = {}
        self._modules = None

    def is_callable(self, name):
        """
        Return true if the callable is available and can be used
        """
        return name in self._callables

    def get(self, name):
        """
        Return the callable by it's name
        """
        return self._callables[name]

    def register(self, function, name=None):
        if not name:
            module = ''.join(str(function.__module__).rsplit('.fragment', 1))
            name = '.'.join((module, function.__name__))

        if ':' in name:
            log.error('Ivalid function name %s.' % name)
            return

        # Check for already registered functions
        if name in self._callables:
            log.error('%s was already registered.' % name)
            return

        # Create the shards function target
        function = ShardTarget(callable=function, name=name)
        print "register", function

        # Register this new ajax function
        self._callables[name] = function

    @property
    def shards(self):
        """
        All shards available
        """
        return self._callables

    @property
    def modules(self):
        """
        Return an easy to loop module hierarchy with all the callables
        """
        if not self._modules:
            self._modules = ShardModule()
            for name, function in self._callables.items():
                self._modules.add(name, function)
        return self._modules


class ShardTarget(object):
    def __init__(self, callable, name):
        """
        Holds a shard callable handler
        """
        self.callable = callable
        self.name = name

    def __str__(self):
        return self.name

    def call(self, *args, **kwargs):
        """
        Call the function or class view
        """
        if inspect.isclass(self.callable):
            if issubclass(self.callable, View):
                return self.callable.as_view()(*args, **kwargs).render()
            else:
                raise InvalidClassViewError("'%s' isn't a valid view class" % self.callable)
        else:
            return self.callable(*args, **kwargs)


class ShardModule(object):
    """
    Helper representation of a shard module
    """

    def __init__(self, name=None):
        self.name = name
        self.callables = {}
        self.submodules = {}

    def add(self, name, function):
        """
        Add this function at the ``name`` deep. If the submodule already
        exists, recusively call the add method into the submodule. If not,
        create the module and call the add method
        """

        # If this is not the final function name (there are more modules)
        # split the name again an register a new submodule.
        if '.' in name:
            module, extra = name.split('.', 1)
            if module not in self.submodules:
                self.submodules[module] = ShardModule(module)
            self.submodules[module].add(extra, function)
        else:
            self.callables[name] = function