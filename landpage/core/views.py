from django.shortcuts import render
from django.conf import settings

from .forms import UserContactForm


def index(request):
    """
    Only render the form
    """
    context = {"cookie_name": 'feedback_cookie'}

    print request.LANGUAGE_CODE
    print settings.LOCALE_PATHS

    if not request.COOKIES.has_key(context["cookie_name"]):
        form = UserContactForm()
        context["form"] = form

    return render(request, "index.html", context)