import django.dispatch

work_read = django.dispatch.Signal(providing_args=["work"])