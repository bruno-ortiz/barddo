import json

from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.html import escape
from django.views.generic import View

from .exceptions import UserNotProvided
from accounts.models import BarddoUser


__author__ = 'bruno'


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('core.views.index'))


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
        context.update(kwargs)
        return super(ProfileAwareView, self).render_to_response(context)


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
    template_name = 'profile.html'
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


class UsernamesAjaxView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        query_paramter = escape(request.GET['q'])
        should_ignore_owner = is_true(request.GET.get('ignore_owner', True))
        user_query_set = BarddoUser.objects.username_startswith(query_paramter)
        if should_ignore_owner:
            user_query_set = user_query_set.differs_from(request.user.id)
        users = user_query_set[:10]
        user_data = map(lambda x: {'id': x.id, 'username': x.username}, users)
        json_data = json.dumps(user_data)
        return HttpResponse(json_data, content_type='application/json')


is_true = lambda value: bool(value) and value.lower() not in ('false', '0')