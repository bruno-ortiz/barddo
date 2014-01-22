from django.shortcuts import render


def index(request):
    context = {}
    if request.user.is_authenticated():
        context['avatar'] = request.user.user_profile.avatar
        context['username'] = request.user.username
    return render(request, "index.html", context)

