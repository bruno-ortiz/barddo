# -*- coding: utf-8 -*-
import hashlib
import os
from hashlib import md5
import time

from django.db import models
from django.db.models import Manager, Count
from django.db.models.query import QuerySet
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models import Q
from django.core.urlresolvers import reverse
from easy_thumbnails.signal_handlers import generate_aliases
from easy_thumbnails.signals import saved_file
from south.modelsinspector import add_introspection_rules

from accounts.models import BarddoUser
from core.exceptions import InvalidFileUploadError
from payments.models import FINISHED_PURCHASE_ID, Purchase
from rating.models import Rating
from search.search_manager import SearchManager


class WorkManager(Manager):
    def get_queryset(self):
        return WorkQuerySet(self.model, using=self._db)

    def total_likes(self):
        return self.get_queryset().total_likes()

    def liked_by(self, user):
        return self.get_queryset().liked_by(user)

    def liked_after(self, date):
        return self.get_queryset().liked_after(date)

    def owned_by(self, user):
        return self.get_queryset().filter(Q(items__purchase__status=FINISHED_PURCHASE_ID, items__purchase__buyer=user) | Q(author=user)).distinct()


class WorkQuerySet(QuerySet):
    def total_likes(self):
        total_likes = Rating.objects.filter(like=True).annotate(work_likes=Count("like")) \
            .values("work_likes").extra(where=["core_work.id = rating_rating.work_id"]).query
        total_likes.group_by = []
        return self.extra(select={"total_likes": total_likes})

    def liked_by(self, user=None):
        if user:
            sub_query = Rating.objects.filter(user=user.id, like=True).annotate(Count('like')).values('like__count') \
                .extra(where=["core_work.id = rating_rating.work_id"]).query
        else:
            sub_query = False

        return self.extra(select={"liked": sub_query})

    def liked_after(self, date):
        return self.filter(Q(like__date__gte=date) | Q(like__isnull=True))


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
    _, ext = os.path.splitext(filename)
    return os.path.join('covers', 'collection', "{0}{1}".format(md5(filename).hexdigest(), ext))


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
    unit = models.ForeignKey(CollectionUnit, null=False, blank=False, db_index=True)

    start_date = models.DateField(_('Start Date'), blank=False, null=False, db_index=True)
    end_date = models.DateField(_('End Date'), blank=True, null=True)

    author = models.ForeignKey(BarddoUser, null=False, db_index=True)
    cover = models.ImageField(_('Cover Art'), upload_to=get_collection_cover_path, blank=True, null=True)

    objects = WorkManager()
    search_manager = SearchManager()

    def get_total_works(self):
        return Work.objects.filter(collection__id=self.id).count()

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

    class Meta:
        index_together = [
            ["name", "summary"],
        ]


def get_work_cover_path(instance, filename):
    """
        Default work cover path
    """
    _, ext = os.path.splitext(filename)
    return os.path.join('covers', 'works',
                        "{0}{1}".format(md5(filename).hexdigest(), ext))


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

    ALLOWED_EXTENSIONS = ['jpg', 'bmp', 'png', 'gif']

    collection = models.ForeignKey(Collection)

    title = models.CharField(_('Title'), max_length=250, db_index=True)
    summary = models.TextField(_('Summary'))
    cover = models.ImageField(_('Cover Art'), upload_to=get_work_cover_path)

    author = models.ForeignKey(BarddoUser, related_name='author_works', db_index=True)

    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True, default=0.0)

    unit_count = models.IntegerField(_('Item Number'), db_index=True)
    total_pages = models.SmallIntegerField(_('Total Pages'))
    publish_date = models.DateTimeField(_('Publish Date'), db_index=True)

    objects = WorkManager()
    search_manager = SearchManager()

    @property
    def pages(self):
        return self.work_pages.order_by('sequence')

    def is_free(self):
        return self.price == 0.0

    def has_pages(self):
        return bool(self.work_pages.count())

    def is_owned_by(self, user):
        return Purchase.objects.is_owned_by(self, user)

    def get_absolute_url(self):
        """
        Detail page url
        """
        return reverse('core.work.detail', args=[str(self.id)])

    def is_owner(self, user):
        """
        Return true if the given user is the owner of the current work
        """
        return self.collection.author.id != user.id

    def media_path(self):
        """
        Return the work directory path on media files
        """
        return os.path.join(settings.MEDIA_ROOT, "work_data", "%04d" % self.id)

    def image_files(self):
        """
        List of image files uploaded for this work
        """
        img_list = os.listdir(self.media_path())

        return sorted([i for i in img_list if any([i.endswith(ext) for ext in self.ALLOWED_EXTENSIONS])])

    def handle_uploaded_file(self, file_name, file):
        """
            Upload a given file to the work media folder
            TODO: object manager?
        """
        full_path = os.path.join(self.media_path(), file_name)
        with open(full_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

    def __unicode__(self):
        return unicode(self.collection) + u" - " + self.title + u" #" + unicode(self.unit_count)

    class Meta:
        unique_together = ("collection", "unit_count")
        index_together = [["title", "summary"], ]

        # TODO: work tags
        # TODO: work categories


def image_storage(instance, filename):
    file_name, file_extension = os.path.splitext(filename)

    # Black list sanity check
    if file_extension.lower()[1:] not in Work.ALLOWED_EXTENSIONS:
        raise InvalidFileUploadError()
    file_name = hashlib.md5(str(time.time())).hexdigest() + file_extension
    return os.path.join("work_data", "%04d" % instance.work.id, file_name)


add_introspection_rules([], ["^core\.models\.AutoIncrementField"])


class AutoIncrementField(models.PositiveIntegerField):
    def pre_save(self, model_instance, add):
        if not add:
            return getattr(model_instance, self.attname)
        return getattr(model_instance, 'next_page_number')


class WorkPage(models.Model):
    sequence = AutoIncrementField()
    work = models.ForeignKey(Work, related_name='work_pages', db_index=True)
    readable_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=image_storage)

    @property
    def next_page_number(self):
        return WorkPage.objects.filter(work=self.work).count()


saved_file.connect(generate_aliases)