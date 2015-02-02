# coding=utf-8
from django.db import transaction
from core.models import CollectionSource


def create_source():
    with transaction.atomic():
        obj, _ = CollectionSource.objects.get_or_create(id=CollectionSource.CENTRAL_DE_MANGAS_ID, defaults={'name': u"Central de Mangás", 'referer': u"www.centraldemangas.net"})
    return obj