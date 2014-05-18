from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin

from shards.decorators import register_shard


@register_shard(name=u"feedback")
class FeedbackModalView(TemplateResponseMixin, View):
    """
    Just create the feedback form modal, if user is logged in, then we use it's information,
    otherwise, we let the user provide email and name
    """
    template_name = 'feedback-modal.html'

    def post(self, request, *args, **kwargs):
        context = {}

        context["username"] = request.user.get_full_name()
        context["email"] = request.user.email

        return super(FeedbackModalView, self).render_to_response(context)