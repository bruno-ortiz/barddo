from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

__author__ = 'bruno'


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('core.views.index'))
