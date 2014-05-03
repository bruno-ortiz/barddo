from functools import wraps

from django.db.models.query import QuerySet
from django.core.exceptions import FieldError
from django.db import models
from django.db import connection
from MySQLdb import OperationalError
from MySQLdb.constants.ER import FT_MATCHING_KEY_NOT_FOUND

# TODO: when needed, detect database type and handle
# More information about this method, see http://www.mercurytide.co.uk/news/article/django-full-text-search/


def _get_indices(model):
    """
    Return all of the FULLTEXT indices available for a given Django model
    """

    cursor = connection.cursor()
    cursor.execute('show index from %s where index_type = "FULLTEXT"' %
                   connection.ops.quote_name(model._meta.db_table))
    found = {}
    item = cursor.fetchone()
    while item:
        if not item:
            break
        (model_name, key_name, column_name) = (item[0], item[2], item[4])
        if not found.has_key(key_name):
            found[key_name] = []
        found[key_name].append(column_name)
        item = cursor.fetchone()

    return found.values()


def _handle_operation(f):
    """
    Specialized wrapper for methods of SearchQuerySet that will
    inform the user of what indices are available, should the user
    specify a list of fields on which to search
    """

    def wrapper(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        except OperationalError, e:
            if e.args[0] != FT_MATCHING_KEY_NOT_FOUND:
                raise

            idc = _get_indices(self.model)
            message = "No FULLTEXT indices found for this table."
            if len(idc) > 0:
                message = ("Index not found.  Indices available include: %s" %
                           str(tuple(idc)))
            raise FieldError, message

    return wraps(f)(wrapper)


class SearchQuerySet(QuerySet):
    """
    A QuerySet with a new method, search, and wrappers around the
    most common operations performed on a query set
    """

    def __init__(self, model=None, query=None, using=None, aggregate_field_name='relevance'):
        super(SearchQuerySet, self).__init__(model, query, using)
        self._aggregate_field_name = aggregate_field_name

    def order_by_relevance(self):
        return self.order_by("-" + self._aggregate_field_name)

    def search(self, query, fields):
        meta = self.model._meta

        if not fields:
            found = _get_indices(self.model)
            if len(found) != 1:
                raise FieldError, "More than one index found for this table."
            fields = found[0]

        columns = [meta.get_field(name, many_to_many=False).column
                   for name in fields]
        full_names = ["%s.%s" % (connection.ops.quote_name(meta.db_table),
                                 connection.ops.quote_name(column))
                      for column in columns]
        match_expr = "MATCH(%s) AGAINST (%%s IN BOOLEAN MODE)" % (", ".join(full_names))

        return self.extra(select={self._aggregate_field_name: match_expr},
                          where=[match_expr],
                          params=[query],
                          select_params=[query])

    # Python Magic Methods wrapped to provide useful information on exception.
    def __repr__(self):
        return super(SearchQuerySet, self).__repr__()

    __repr__ = _handle_operation(__repr__)

    def __len__(self):
        return super(SearchQuerySet, self).__len__()

    __len__ = _handle_operation(__len__)

    def __iter__(self):
        return super(SearchQuerySet, self).__iter__()

    __iter__ = _handle_operation(__iter__)

    def _result_iter(self):
        return super(SearchQuerySet, self)._result_iter()

    _result_iter = _handle_operation(_result_iter)

    def __nonzero__(self):
        return super(SearchQuerySet, self).__nonzero__()

    __nonzero__ = _handle_operation(__nonzero__)

    def __getitem__(self, k):
        return super(SearchQuerySet, self).__getitem__(k)

    __getitem__ = _handle_operation(__getitem__)

    # This is a private method of QuerySet.  It's not guaranteed to even exist
    # after Django 1.2

    def _fill_cache(self, *args, **kwargs):
        return super(SearchQuerySet, self)._fill_cache(*args, **kwargs)

    _fill_cache = _handle_operation(_fill_cache)


class SearchManager(models.Manager):
    """
    Custom object manager to handle fulltext searches
    """

    def get_query_set(self, fields=[]):
        """
        Custom queryset
        """
        return SearchQuerySet(self.model)

    def search(self, query, fields=[]):
        """
        Search using fulltext search indexes, fields aren't really required,
        if none given, then a search will happen on every database FTS field
        """
        return self.get_query_set().search(query, fields)

    def search_ordered(self, query, fields=[]):
        """
        Ordered search using fulltext search indexes, fields aren't really required,
        if none given, then a search will happen on every database FTS field.

        The order is determined by search relevancy.
         i.e: search for "the +great" means the only required word is 'great', but matches with 'the' will boost
         relevancy if found
        """
        return self.search(query, fields).order_by_relevance()