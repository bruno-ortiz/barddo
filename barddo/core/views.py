from django.shortcuts import render


def index(request):
    return render(request, "index.html")

###
### Collection related views
###


def collection_list(request):
    return render(request, "index.html")


def collection_create(request):
    return render(request, "collection_create.html")