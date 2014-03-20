import json

from django.http.response import StreamingHttpResponse
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin

from core.views import ProfileAwareView, LoginRequiredMixin
from publishing.models import Country
from shards.decorators import register_shard


__author__ = 'bruno'


class PublisherLandpage(LoginRequiredMixin, ProfileAwareView):
    template_name = 'publisher_landpage.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        is_barddo_publisher = user.is_barddo_publisher()
        context = {'barddo_publisher': is_barddo_publisher}
        return super(PublisherLandpage, self).get(request, **context)


publisher_landpage = PublisherLandpage.as_view()


@register_shard(name=u'join.barddo')
class JoinBarddoModal(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'join_barddo_modal.html'

    def post(self, *args, **kwargs):
        return super(JoinBarddoModal, self).render_to_response({})


@register_shard(name=u'create.group')
class CreateGroupModal(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'create_group_modal.html'

    def post(self, *args, **kwargs):
        return super(CreateGroupModal, self).render_to_response({})


class CountriesAjaxView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        countries = Country.objects.all()
        countries = map(lambda x: {'id': x.id, 'text': x.country_name}, countries)
        data = json.dumps(countries)
        return StreamingHttpResponse(data, content_type='application/json')