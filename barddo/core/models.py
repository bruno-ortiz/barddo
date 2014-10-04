# -*- coding: utf-8 -*-
import hashlib
import os
from hashlib import md5
import time

from PIL import Image
from django.db import models
from django.db import transaction
from django.db.models import Manager, Count, F
from django.db.models.query import QuerySet
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models import Q
from django.core.urlresolvers import reverse
from easy_thumbnails.signal_handlers import generate_aliases
from easy_thumbnails.signals import saved_file
from south.modelsinspector import add_introspection_rules
from easy_thumbnails.files import get_thumbnailer
from taggit.managers import TaggableManager

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
        return self.get_queryset().filter(
            Q(items__purchase__status=FINISHED_PURCHASE_ID, items__purchase__buyer=user) | Q(author=user)).distinct()


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

    start_date = models.DateField(_('Start Date'), blank=False, null=False, db_index=True)
    end_date = models.DateField(_('End Date'), blank=True, null=True)

    author = models.ForeignKey(BarddoUser, null=False, db_index=True)

    extra_data = models.CharField(_('Extra Data'), max_length=100, db_index=True, blank=True, null=True)  # TODO rever D:

    cover = models.ImageField(_('Cover Art'), upload_to=get_collection_cover_path, blank=True, null=True)
    cover_url = models.URLField(_('Remote Cover Url'), blank=True, null=True)

    objects = WorkManager()
    search_manager = SearchManager()
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        """
        The collection slug is always based on it's first name.
        This will only create a new slug, there's no need to update with collection name
        """
        if not self.id:
            self.slug = slugify(self.name)

        super(Collection, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Detail page url
        """
        return reverse('core.collection.detail', args=[str(self.slug)])

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
                        u"{0}{1}".format(md5(filename.encode('utf-8')).hexdigest(), ext))


class Work(models.Model):
    """
    A work is a semantic item of a collection. Their name shouldn't be equals to the collection, and
    it' artists can only be from the collection list.
    Eg.
        - Collection is 'One Piece', a work should be 'Chapter 01 - My name is Luffy'
        - Collection artists: "Israel" and "Bruno", being "Israel" author of the 1st volume and "Bruno" the other
        - A work made by two artists: "Israel" the writer and "Bruno", the painter
    """

    ALLOWED_EXTENSIONS = ['jpg', 'bmp', 'png', 'gif']

    collection = models.ForeignKey(Collection, related_name="works")

    title = models.CharField(_('Title'), max_length=250, db_index=True)
    slug = models.SlugField(_('Slug'), max_length=250, db_index=True)

    summary = models.TextField(_('Summary'))
    cover = models.ImageField(_('Cover Art'), upload_to=get_work_cover_path, null=True, blank=True)
    cover_url = models.URLField(_('Remote Cover Url'), blank=True, null=True)

    author = models.ForeignKey(BarddoUser, related_name='author_works', db_index=True)

    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True, default=0.0)

    unit_count = models.IntegerField(_('Item Number'), db_index=True)
    total_pages = models.SmallIntegerField(_('Total Pages'))
    publish_date = models.DateTimeField(_('Publish Date'), db_index=True)

    is_published = models.BooleanField(_('Is Published?'), db_index=True, default=False)

    objects = WorkManager()
    search_manager = SearchManager()

    @property
    def pages(self):
        return self.work_pages.order_by('sequence')

    def get_best_page_ratio(self):
        """
        Determina qual a melhor página para configurar o aspect ratio (width/height) de exibição. Este valor é usado na
        hora de determinar como redimensionar as imagens exibidas no leitor, caso as imagens não tenham tamanho uniforme

        :rtype: float
        :return: aspect ratio da página mais alta do trabalho
        """
        w, h = 1, 1

        # Escolhe as maiores dimensões, baseando-se sempre na altura, que é o que mais determina
        # a forma como o quadrinho é exibido no monitor do usuário
        for page in self.pages:
            if page.image.height > h:
                w = page.image.width
                h = page.image.height

        return str(float(w) / float(h))

    def add_page(self, page_file):
        """
        Adds a page to this work

        :param page_file: The page file
        :type page_file: file
        :return: the created WorkPage
        :rtype: WorkPage
        """
        return WorkPage.objects.create(work=self, image=page_file, readable_name=page_file.name)

    def move_page(self, pos_from, pos_to):
        """
        Move uma pagina de posição

        :param pos_from: Posição inicial da página
        :type pos_from: int
        :param pos_to:  Posição para a qual a página será movida.
        :type pos_to: int
        """
        with transaction.atomic():
            page = WorkPage.objects.get(work=self, sequence=pos_from)
            if pos_from > pos_to:
                WorkPage.objects.filter(Q(sequence__gte=pos_to) & Q(sequence__lt=pos_from), work=self).update(
                    sequence=F('sequence') + 1)
            else:
                WorkPage.objects.filter(Q(sequence__gt=pos_from) & Q(sequence__lte=pos_to), work=self).update(
                    sequence=F('sequence') - 1)
            page.sequence = pos_to
            page.save()

    def remove_page(self, page_index):
        """
        Remove a página do banco

        :param page_index: Indice da página a ser removida
        :type page_index: int
        """
        with transaction.atomic():
            WorkPage.objects.get(work=self, sequence=page_index).delete()
            WorkPage.objects.filter(work=self, sequence__gt=page_index).update(sequence=F('sequence') - 1)

    def is_free(self):
        return self.price == 0.0

    def has_pages(self):
        return bool(self.work_pages.count()) or bool(self.remote_pages.count())

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
        return self.collection.author.id == user.id or self.author.id == user.id

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

    def save(self, *args, **kwargs):
        """
        The work slug is always based on it's first name.
        This will only create a new slug, there's no need to update with collection name
        """
        if not self.id:
            self.slug = slugify(self.title)

        super(Work, self).save(*args, **kwargs)

    def get_thumbnail_sprite_file(self):
        """
        :rtype: str
        :return: retorna o nome completo do arquivo de thumbs atrelado a este trabalho
        """
        return os.path.join(settings.MEDIA_ROOT, "sprites", "{}-sprited-thumbs.png".format(self.id))

    def get_thumbnail_url(self):
        """
        Retorna a url do arquivo de thumbs atrelados ao trabalho. Caso ele não exista, um novo será criado.

        Existem sinais que invalidam este arquivo caso alguma página tenha sido alterada ou removida.

        :rtype: str
        :return: url do arquivo de thumbs
        """
        thumbs_url = self.get_thumbnail_sprite_file()

        if not os.path.exists(thumbs_url):
            thumb_width, thumb_height = settings.THUMBNAIL_ALIASES['core.WorkPage.image']['reader_thumbs']['size']
            thumb_images = [page.image for page in self.pages]

            sprited_thumbs = Image.new("RGB", (thumb_width, thumb_height * len(thumb_images)))
            for x in xrange(len(thumb_images)):
                current_image = get_thumbnailer(thumb_images[x])['reader_thumbs']
                # current_path = current_path.replace(settings.MEDIA_URL, settings.MEDIA_ROOT + '/')
                current = Image.open(current_image.path)
                sprited_thumbs.paste(current, (0, x * thumb_height))

            with open(thumbs_url, "wb") as thumb_sprites_file:
                sprited_thumbs.save(thumb_sprites_file)

        return settings.MEDIA_URL + thumbs_url.replace(settings.MEDIA_ROOT + "/", "")

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


class RemotePage(models.Model):
    sequence = models.PositiveIntegerField(_("Page Sequence"))
    work = models.ForeignKey(Work, related_name='remote_pages', db_index=True)
    url = models.URLField(blank=True, null=True)