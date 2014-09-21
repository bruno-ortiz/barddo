import json

from django.conf import settings
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
from social.backends.google import GooglePlusAuth

from .exceptions import UserNotProvided
from accounts.models import BarddoUser
from follow.models import Follow
from feed.models import UserFeed


# #
# Mixins
# #
from notifications.models import Notification


class LoginRequiredMixin(object):
    """
    Mixin to be used on login required views composition
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class ProfileAwareView(ContextMixin, TemplateResponseMixin, View):
    """
    To be used on views that require user profile on it's composition
    """

    def get(self, request, *args, **kwargs):
        user = request.user
        context = self.get_context_data(**{'user': user})
        context.update(kwargs)
        return super(ProfileAwareView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = {}
        if 'user' not in kwargs:
            raise UserNotProvided(_('User not provided'))

        user = kwargs['user']
        if user.is_authenticated():
            context['avatar'] = user.profile.avatar
            context['username'] = user.username
            kwargs['notifications'] = Notification.objects.filter(recipient=user).unread()[:6]
        else:
            plus_scope = ' '.join(GooglePlusAuth.DEFAULT_SCOPE)  # TODO: Mover para um GoogleAuthMixin?
            plus_id = settings.SOCIAL_AUTH_GOOGLE_PLUS_KEY
            context['plus_scope'] = plus_scope
            context['plus_id'] = plus_id
        context.update(kwargs)
        return super(ProfileAwareView, self).get_context_data(**context)


# #
# Authentication Views
# #
class LogoutView(View):
    """
    User logout from system
    """

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('core.index'))


class UserProfileView(LoginRequiredMixin, SingleObjectMixin, ProfileAwareView):
    """
    This view is responsible for rendering the user profile,
    it makes some verifications, to avoid that a user edits another user profile.
    """
    template_name = 'profile.html'
    model = BarddoUser
    editable = False

    def get(self, request, *args, **kwargs):
        current_user = request.user
        if not self.editable:
            profile_user = self.get_object()
            self.editable = profile_user.id == current_user.id
        else:
            profile_user = current_user

        following = Follow.objects.following(profile_user, BarddoUser)
        followers = Follow.objects.followers(profile_user)
        context = {'user': current_user,
                   'viewing_user': profile_user,
                   'viewing_user_profile': profile_user.profile,
                   'editable': self.editable,
                   'following': following,
                   'followers': followers,
                   'user_feed': UserFeed.objects.feed_for_user(profile_user),
                   'profile_notifications': Notification.objects.prefetch_related('actor', 'action_object', 'target').filter(recipient=profile_user).all()}
        if current_user != profile_user:
            follows = Follow.objects.follows(current_user, profile_user)
            context['follows'] = follows
        context = ProfileAwareView.get_context_data(self, **context)
        return super(UserProfileView, self).render_to_response(context)


# #
# Ajax views
# #
_is_true = lambda value: bool(value) and value.lower() not in ('false', '0')


class UsernamesAjaxView(LoginRequiredMixin, View):
    """
    Handle username matching for auto complete
    """

    SUGGESTIONS_LIMIT = 10

    def get(self, request, *args, **kwargs):
        query_paramter = escape(request.GET['q'])
        should_ignore_owner = _is_true(request.GET.get('ignore_owner', "true"))
        user_query_set = BarddoUser.objects.username_startswith(query_paramter)

        if should_ignore_owner:
            user_query_set = user_query_set.differs_from(request.user.id)

        users = user_query_set[:self.SUGGESTIONS_LIMIT]
        user_data = map(lambda x: {'id': x.id, 'username': x.username}, users)
        json_data = json.dumps(user_data)
        return HttpResponse(json_data, content_type='application/json')


