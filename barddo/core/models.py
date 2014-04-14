# -*- coding: utf-8 -*-
import os
from hashlib import md5
import time

from django.db import models
from django.db.models import Manager, Count
from django.db.models.query import QuerySet
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.files.images import ImageFile
from django.db.models import Q
from easy_thumbnails.files import get_thumbnailer

from accounts.models import BarddoUser
from rating.models import Rating


class RatingManager(Manager):
    def get_queryset(self):
        return RatingQuerySet(self.model, using=self._db)

    def total_likes(self):
        return self.get_queryset().total_likes()

    def liked_by(self, user):
        return self.get_queryset().liked_by(user)

    def liked_after(self, date):
        return self.liked_after(date)


class RatingQuerySet(QuerySet):
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
    unit = models.ForeignKey(CollectionUnit, null=False, blank=False)

    start_date = models.DateField(_('Start Date'), blank=False, null=False)
    end_date = models.DateField(_('End Date'), blank=True, null=True)

    author = models.ForeignKey(BarddoUser, null=False)
    cover = models.ImageField(_('Cover Art'), upload_to=get_collection_cover_path, blank=True, null=True)

    objects = RatingManager()

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

    author = models.ForeignKey(BarddoUser, related_name='author_works')

    unit_count = models.IntegerField(_('Item Number'))
    total_pages = models.SmallIntegerField(_('Total Pages'))
    publish_date = models.DateTimeField(_('Publish Date'))

    objects = RatingManager()

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

    def load_work_pages(self):
        """
        Return a dict with loaded images data to be rendered
        Example dict: {
            "size": 123,
            "url": /media/all/black_flag.png,
            "name": black_flag.png
        }
        """
        work_path = self.media_path()

        # Sanity directory check
        if not os.path.exists(work_path):
            return []

        files = self.image_files()

        timestamp = "%d" % time.time()  # a little hack to avoid browser caching issues
        image_files = []

        for image_file in files:
            img = ImageFile(open(os.path.join(work_path, image_file), "rb"))
            image_files.append({
                "size": img.size,
                "url": settings.MEDIA_URL + img.name.replace(settings.MEDIA_ROOT + "/", "") + "?t=" + timestamp,
                "name": image_file
            })

        return image_files

    def load_work_pages_without_timestamp(self):
        """
        Return a dict with loaded images data to be rendered
        Example dict: {
            "size": 123,
            "url": /media/all/black_flag.png,
            "name": black_flag.png
        }
        """
        work_path = self.media_path()

        # Sanity directory check
        if not os.path.exists(work_path):
            return []

        files = self.image_files()

        image_files = []

        for image_file in files:
            img = ImageFile(open(os.path.join(work_path, image_file), "rb"))
            image_files.append({
                "size": img.size,
                "url": settings.MEDIA_URL + img.name.replace(settings.MEDIA_ROOT + "/", ""),
                "name": image_file,
                "thumb": get_thumbnailer(img, relative_name=os.path.join("work_data", "%04d" % self.id, 'thumb', image_file))
            })

        return image_files

    class Meta:
        unique_together = (("collection", "unit_count"))

        # TODO: work tags
        # TODO: work categories
        # TODO: store files by convention

