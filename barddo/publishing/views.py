import json

from django.http.response import HttpResponse

from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin

from core.views import ProfileAwareView, LoginRequiredMixin
from publishing.models import Country
from shards.decorators import register_shard


__author__ = 'bruno'


class PublisherLandpage(LoginRequiredMixin, ProfileAwareView):
    template_name = 'publisher_landpage.html'


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
    def get(self, request, *args, **kwargs):
        countries = []
        query_parameter = request.GET['q'].lower()
        for country in Country.objects.all():
            if country.country_name.lower().startswith(query_parameter):
                countries.append(country.country_name)
        data = json.dumps(countries)
        return HttpResponse(data, mimetype='application/json')