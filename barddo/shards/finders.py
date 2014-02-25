import os
import tempfile

from django.contrib.staticfiles import finders
from django.template import Context
from django.template.loader import get_template
from django.core.exceptions import SuspiciousOperation


class VirtualStorage(finders.FileSystemStorage):
    """"
    Mock a FileSystemStorage to build tmp files on demand.
    Based on DAJAXICE implementation.
    """

    def __init__(self, *args, **kwargs):
        self._files_cache = {}
        super(VirtualStorage, self).__init__(*args, **kwargs)

    def get_or_create_file(self, path):
        if path not in self.files:
            return ''

        data = getattr(self, self.files[path])()

        try:
            current_file = open(self._files_cache[path])
            current_data = current_file.read()
            current_file.close()
            if current_data != data:
                os.remove(path)
                raise Exception("Invalid data")
        except Exception:
            handle, tmp_path = tempfile.mkstemp()
            tmp_file = open(tmp_path, 'w')
            tmp_file.write(data)
            tmp_file.close()
            self._files_cache[path] = tmp_path

        return self._files_cache[path]

    def exists(self, name):
        return name in self.files

    def listdir(self, path):
        folders, files = [], []
        for f in self.files:
            if f.startswith(path):
                f = f.replace(path, '', 1)
                if os.sep in f:
                    folders.append(f.split(os.sep, 1)[0])
                else:
                    files.append(f)
        return folders, files

    def path(self, name):
        try:
            path = self.get_or_create_file(name)
        except ValueError:
            raise SuspiciousOperation("Attempted access to '%s' denied." % name)
        return os.path.normpath(path)


class ShardsStorage(VirtualStorage):
    """
    Map specific module resources as static content
    """
    files = {os.path.join('shards', 'shards.js'): 'shards_js'}

    def shards_js(self):
        from shards.core import shards_core

        c = Context({'shard_manager': shards_core})
        return get_template(os.path.join('shards', 'shards.js')).render(c)


class ShardsFinder(finders.BaseStorageFinder):
    """
    Finder to the module static resources
    """
    storage = ShardsStorage()