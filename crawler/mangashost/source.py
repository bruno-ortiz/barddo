# coding=utf-8
from django.db import transaction
from core.models import CollectionSource


def create_source():
    with transaction.atomic():
        obj, _ = CollectionSource.objects.get_or_create(id=2, name=u"Mangás Host", referer=u"http://mangashost")
    return obj