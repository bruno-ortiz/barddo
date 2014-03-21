import json

from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.html import escape
from django.views.generic import View

from accounts.models import BarddoUser
from core.views import LoginRequiredMixin


__author__ = 'bruno'


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('core.views.index'))


class UsernamesAjaxView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        query_paramter = escape(request.GET['q'])
        users = BarddoUser.objects.username_startswith(query_paramter).differs_from(request.user.id)[:6]
        user_data = map(lambda x: {'id': x.id, 'username': x.username}, users)
        json_data = json.dumps(user_data)
        return HttpResponse(json_data, content_type='application/json')
