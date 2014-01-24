from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import CollectionForm

# TODO: refactor this thing so we dont need to pass it every view request
def create_user_context(request):
    context = {}
    if request.user.is_authenticated():
        context['avatar'] = request.user.user_profile.avatar
        context['username'] = request.user.username
    return context


def index(request):
    return render(request, "index.html", create_user_context(request))


###
### Collection related views
###

@login_required
def collection_list(request):
    # TODO: implement
    return render(request, "index.html")

@login_required
def collection_create(request):
    context = create_user_context(request)
    context['form'] = CollectionForm()
    return render(request, "collection_create.html", context)