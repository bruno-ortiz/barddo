from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from .forms import CollectionForm


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


index = IndexView.as_view()

###
### Collection related views
###


class CreateCollectionView(LoginRequiredMixin, ProfileAwareView):
    template_name = 'collection_create.html'

    def get_context_data(self, **kwargs):
        context = {'form': CollectionForm()}
        context.update(kwargs)
        return super(CreateCollectionView, self).get_context_data(**context)


create_collection = CreateCollectionView.as_view()


@login_required
def collection_list(request):
    # TODO: implement
    return render(request, "index.html")
