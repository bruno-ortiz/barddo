from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin

from shards.decorators import register_shard


@register_shard(name=u"feedback")
class FeedbackModalView(TemplateResponseMixin, View):
    template_name = 'feedback-modal.html'

    def post(self, *args, **kwargs):
        return super(FeedbackModalView, self).render_to_response({})