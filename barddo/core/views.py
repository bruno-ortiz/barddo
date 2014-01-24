from django.shortcuts import render
from .forms import CollectionForm


def index(request):
    context = {}
    if request.user.is_authenticated():
        context['avatar'] = request.user.user_profile.avatar
        context['username'] = request.user.username
    return render(request, "index.html", context)


###
### Collection related views
###


def collection_list(request):
    return render(request, "index.html")


def collection_create(request):
    form = CollectionForm()
    return render(request, "collection_create.html", {'form': form})