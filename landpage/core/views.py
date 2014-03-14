from django.shortcuts import render

from .forms import UserContactForm


def index(request):
    """
    Only render the form
    """
    context = {"cookie_name": 'feedback_cookie'}

    if not request.COOKIES.has_key(context["cookie_name"]):
        form = UserContactForm()
        context["form"] = form

    return render(request, "index.html", context)