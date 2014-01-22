from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required()
def logged(request):
    avatar = request.user.user_profile.avatar
    username = request.user.username
    return render(request, "index.html", {'avatar': avatar, 'username': username})

