import django.dispatch

work_liked = django.dispatch.Signal(providing_args=['work_id'])