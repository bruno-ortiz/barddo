from django.shortcuts import render
from .forms import CollectionForm


def index(request):
    return render(request, "index.html")

###
### Collection related views
###


def collection_list(request):
    return render(request, "index.html")


def collection_create(request):
    form = CollectionForm()
    return render(request, "collection_create.html", {'form': form})