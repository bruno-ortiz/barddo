from django.views.generic.base import TemplateResponseMixin, View

from shards.decorators import register_shard


@register_shard(name=u"modal.new.collection")
class NewCollectionModalView(TemplateResponseMixin, View):
    """
        Render a simple collection modal. This is incomplete, another shard will be used to render a work detail.
    """
    template_name = '_new_collection_modal.html'

    def get(self, request, *args, **kwargs):
        context = {
        }
        return super(NewCollectionModalView, self).render_to_response(context)