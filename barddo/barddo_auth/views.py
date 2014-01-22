from django.contrib.auth import logout
from django.shortcuts import render

__author__ = 'bruno'


def logout_user(request):
    logout(request)
    return login(request)


def login(request):
    return render(request, "index.html")