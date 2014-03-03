from core.views import ProfileAwareView, LoginRequiredMixin

__author__ = 'bruno'


class PublisherLandpage(LoginRequiredMixin, ProfileAwareView):
    template_name = 'publisher_landpage.html'


publisher_landpage = PublisherLandpage.as_view()