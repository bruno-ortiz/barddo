# -*- coding: utf-8 -*-
import os
from hashlib import md5
import time

from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.files.images import ImageFile

from accounts.models import BarddoUser


class CollectionUnit(models.Model):
    """
    A collection can have any type of units types. This entity represents this possibility.
    Eg.
        - Chapters
        - Volumes
        - Pages
    """
    description = models.CharField(_('Description'), max_length=250, unique=True)

    def __unicode__(self):
        return self.description


def get_collection_cover_path(instance, filename):
    """
        Default work cover path
    """
    return os.path.join('covers', 'collection', md5(filename).hexdigest())


class Collection(models.Model):
    """
    A collection is a catalog of works from one or more artists.
    Eg.
        - One Piece is a collection of 72 works (in this case, volumes) by Eiichiro Oda
        - Gantz is a collection of 37 works (in this case, volumes) by Hiroya Oku
        - Amagami is a collection from various artists works
    """

    STATUS_ONGOING = 0
    STATUS_COMPLETED = 1
    STATUS_STOPPED = 2
    STATUS_CHOICES = (
        (STATUS_ONGOING, _('On Going')),
        (STATUS_COMPLETED, _('Completed')),
        (STATUS_STOPPED, _('Stopped')),
    )

    name = models.CharField(_('Collection Name'), max_length=250, unique=True)
    summary = models.TextField(_('Summary'))

    slug = models.SlugField(_('Slug'), max_length=250, db_index=True)
    status = models.SmallIntegerField(_('Status'), choices=STATUS_CHOICES, default=STATUS_ONGOING, db_index=True)
    unit = models.ForeignKey(CollectionUnit)

    start_date = models.DateField(_('Start Date'), blank=False, null=False)
    end_date = models.DateField(_('End Date'), blank=True, null=True)

    author = models.ForeignKey(BarddoUser, null=False)
    cover = models.ImageField(_('Cover Art'), upload_to=get_collection_cover_path, blank=True, null=True)

    # TODO: collection tags
    # TODO: collection categories

    def save(self, *args, **kwargs):
        """
        The collection slug is always based on it's first name.
        This will only create a new slug, there's no need to update with collection name
        """
        if not self.id:
            self.slug = slugify(self.name)

        super(Collection, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


def get_work_cover_path(instance, filename):
    """
        Default work cover path
    """
    return os.path.join('covers', 'works', md5(filename).hexdigest())


class Work(models.Model):
    """
    A work is a semantic item of a collection. Their name shouldn't be equals to the collection, and
    it' artists can only be from the collection list.
    Eg.
        - Collection is 'One Piece', a work should be 'Chapter 01 - My name is Luffy'
        - Collection artists: "Israel" and "Bruno", being "Israel" author of the 1st volume and "Bruno" the other
        - A work made by two artists: "Israel" the writer and "Bruno", the painter

    Work files will be stored by convention.
    Eg.
        - Collection 01
            - Work 01
                - Page 01
                - Page 02
            - Work 01
                - Page 01
                - Page 02
            ...
        ...
    """

    collection = models.ForeignKey(Collection)

    title = models.CharField(_('Title'), max_length=250, db_index=True)
    summary = models.TextField(_('Summary'))
    cover = models.ImageField(_('Cover Art'), upload_to=get_work_cover_path)

    unit_count = models.IntegerField(_('Item Number'))
    total_pages = models.SmallIntegerField(_('Total Pages'))

    def list_work_files(self, work_path):
        img_list = os.listdir(work_path)
        allowed_extensions = ['jpg', 'bmp', 'png', 'gif']
        return sorted([i for i in img_list if any([i.endswith(ext) for ext in allowed_extensions])])

    def load_work_pages(self):
        work_path = os.path.join(settings.MEDIA_ROOT, "work_data", "%04d" % self.id)
        if not os.path.exists(work_path):
            return []

        files = self.list_work_files(work_path)

        image_files = []
        timestamp = "%d" % time.time()
        for file in files:
            img = ImageFile(open(os.path.join(work_path, file), "rb"))
            image_files.append({
                "size": img.size,
                "url": settings.MEDIA_URL + img.name.replace(settings.MEDIA_ROOT + "/", "") + "?t=" + timestamp,
                "name": file
            })

        return image_files

    class Meta:
        unique_together = (("collection", "unit_count"), ("collection", "title"))

        # TODO: work tags
        # TODO: work categories
        # TODO: store files by convention
