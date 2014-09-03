# coding=utf-8

from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from django.db.models import Max
from django.db.models import Q

from core.signals import work_read

from shards.decorators import register_shard
from .forms import CollectionForm, WorkForm, CoverOnlyWorkForm
from .models import Collection, Work


@register_shard(name=u"reader")
class ReaderShard(TemplateResponseMixin, View):
    """
        Render a simple reader.
    """

    @staticmethod
    def can_read(user, work):
        return work.is_free() or work.is_owned_by(user) or user.is_staff or work.author == user

    def post(self, request, work_id, *args, **kwargs):
        work = Work.objects.get(pk=work_id)
        suggestions = list(Work.objects.filter(~Q(id=work_id), is_published=True).order_by('?')[:6])
        context = {}
        if self.can_read(request.user, work):
            self.template_name = 'reader/reader-modal.html'
            work_read.send(request.user, work=work)
            context["suggestions_first"] = suggestions[:3]
            context["suggestions_second"] = suggestions[3:]
        else:
            self.template_name = 'payments/buy-work-modal.html'
        context["work"] = work
        return super(ReaderShard, self).render_to_response(context)


@register_shard(name=u"modal.collection")
class CollectionModalView(TemplateResponseMixin, View):
    """
        Render a simple collection modal. This is incomplete, another shard will be used to render a work detail.
    """
    template_name = 'modals/collection.html'

    def post(self, request, collection_id, *args, **kwargs):
        collection = Collection.objects.get(id=collection_id)
        works = Work.objects.filter(collection_id=collection_id).order_by("-unit_count")

        context = {
            "collection": collection,
            "works": works,
            "current_work": works[0],
            'work_form': CoverOnlyWorkForm(works[0])
        }
        return super(CollectionModalView, self).render_to_response(context)


@register_shard(name=u"modal.new.collection")
class NewCollectionModalView(TemplateResponseMixin, View):
    """
        Render a simple collection modal. This is incomplete, another shard will be used to render a work detail.
    """
    template_name = '_new_collection_modal.html'

    def post(self, request, *args, **kwargs):
        context = {
            'form': CollectionForm(),
        }
        return super(NewCollectionModalView, self).render_to_response(context)


@register_shard(name=u"modal.new.work")
class NewWorkModalView(TemplateResponseMixin, View):
    """
        Render a simple collection modal. This is incomplete, another shard will be used to render a work detail.
    """
    template_name = '_new_work_modal.html'

    def post(self, request, collection_id, *args, **kwargs):
        max_unit = Work.objects.filter(collection_id=collection_id).aggregate(Max("unit_count"))['unit_count__max']

        if max_unit == None:
            max_unit = 1
        else:
            max_unit += 1

        context = {
            'next_unit': max_unit,
            'work_form': WorkForm(),
        }
        return super(NewWorkModalView, self).render_to_response(context)


@register_shard(name=u"modal.work")
class WorkModalView(TemplateResponseMixin, View):
    """
        Render a work detail modal shard.
    """
    template_name = 'modals/work_detail.html'

    def post(self, request, work_id, *args, **kwargs):
        work = Work.objects.select_related("collection").get(id=work_id)

        context = {
            "collection": work.collection,
            "current_work": work,
            "work_form": CoverOnlyWorkForm(work)
        }
        return super(WorkModalView, self).render_to_response(context)


@register_shard(name=u"modal.help.discover")
class HelpDiscoverModalView(TemplateResponseMixin, View):
    """
        Render a work detail modal shard.
    """
    template_name = 'help/modal-discover.html'

    def post(self, request, *args, **kwargs):
        return super(HelpDiscoverModalView, self).render_to_response({})


@register_shard(name=u"modal.help.understand")
class HelpUnderstandModalView(TemplateResponseMixin, View):
    """
        Render a work detail modal shard.
    """
    template_name = 'help/modal-understand.html'

    def post(self, request, *args, **kwargs):
        return super(HelpUnderstandModalView, self).render_to_response({})


@register_shard(name=u"modal.help.enjoy")
class HelpEnjoyModalView(TemplateResponseMixin, View):
    """
        Render a work detail modal shard.
    """
    template_name = 'help/modal-enjoy.html'

    def post(self, request, *args, **kwargs):
        return super(HelpEnjoyModalView, self).render_to_response({})
