from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.views.generic.detail import SingleObjectMixin
from accounts.models import BarddoUser
from .forms import CollectionForm, WorkForm
from .models import Collection, Work


class UserNotProvided(Exception):
    pass


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class UserContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):

        context = {}
        if 'user' not in kwargs:
            raise UserNotProvided(_('User not provided'))
        user = kwargs['user']
        if user.is_authenticated():
            context['avatar'] = user.user_profile.avatar
            context['username'] = user.username
        context.update(kwargs)
        return super(UserContextMixin, self).get_context_data(**context)


class ProfileAwareView(UserContextMixin, TemplateResponseMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**{'user': request.user})
        return super(ProfileAwareView, self).render_to_response(context)


class IndexView(ProfileAwareView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        next_url = request.GET.get('next', '')

        works = Work.objects.select_related("collection").all()

        context = self.get_context_data(**{'user': request.user, "next_url": next_url, "works": works})
        return super(IndexView, self).render_to_response(context)

index = IndexView.as_view()

###
### Artist Dashboard
###


class ArtistDashboardView(LoginRequiredMixin, ProfileAwareView):
    template_name = 'artist_dashboard.html'

    def get_context_data(self, **kwargs):
        collections = Collection.objects.filter(author_id=kwargs['user'].id)

        context = {
            'form': CollectionForm(),
            'work_form': WorkForm(),
            'collections': collections
        }
        context.update(kwargs)
        return super(ArtistDashboardView, self).get_context_data(**context)

artist_dashboard = ArtistDashboardView.as_view()


class CollectionDetailView(LoginRequiredMixin, ProfileAwareView):
    template_name = 'collection_detail.html'

    def get(self, request, collection_id, *args, **kwargs):
        collection = Collection.objects.get(id=collection_id)
        works = Work.objects.filter(collection_id=collection_id)

        context = {
            'collection': collection,
            'works': works
        }

        return super(CollectionDetailView, self).render_to_response(context)

collection_detail = CollectionDetailView.as_view()


class UserProfileMixin(SingleObjectMixin, UserContextMixin):
    model = BarddoUser

    def get_context_data(self, **kwargs):
        profile_user = kwargs.get('profile_user')
        if not profile_user:
            profile_user = self.get_object()
        context = {}
        if profile_user:
            context['viewing_user'] = profile_user
            context['viewing_user_profile'] = profile_user.user_profile
            context['editable'] = kwargs.get('editable', False)
        context.update(kwargs)
        return UserContextMixin.get_context_data(self, **context)


class UserProfileView(LoginRequiredMixin, UserProfileMixin, TemplateResponseMixin, View):
    """
        This view is responsible for rendering the user profile,
        it makes some verifcations, to avoid that a user edits another user profile.
    """
    template_name = 'profile/profile.html'
    editable = False

    def get(self, request, *args, **kwargs):
        current_user = request.user
        if not self.editable:
            profile_user = self.get_object()
            self.editable = profile_user.id == current_user.id
        else:
            profile_user = current_user
        context = {'user': current_user, 'profile_user': profile_user, 'editable': self.editable}
        context = self.get_context_data(**context)
        return super(UserProfileView, self).render_to_response(context)


profile = UserProfileView.as_view()
editable_profile = UserProfileView.as_view(editable=True)
# profile = ProfileAwareView.as_view(template_name='profile/profile.html')


class CollectionModalView(TemplateResponseMixin, View):
    template_name = 'modals/collection.html'

    def get(self, request, collection_id, *args, **kwargs):
        collection = Collection.objects.get(id=collection_id)
        works = Work.objects.filter(collection_id=collection_id).order_by("-unit_count")

        context = {
            "collection": collection,
            "works": works,
            "current_work": works[0]
        }
        return super(CollectionModalView, self).render_to_response(context)

render_collection_modal = CollectionModalView.as_view()


class WorkModalView(TemplateResponseMixin, View):
    template_name = 'modals/collection_detail.html'

    def get(self, request, work_id, *args, **kwargs):
        work = Work.objects.select_related("collection").get(id=work_id)

        context = {
            "collection": work.collection,
            "current_work": work
        }
        return super(WorkModalView, self).render_to_response(context)

render_work_modal = WorkModalView.as_view()