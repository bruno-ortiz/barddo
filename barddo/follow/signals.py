import django.dispatch

start_follow = django.dispatch.Signal(providing_args=["follower", "followed"])
stop_follow = django.dispatch.Signal(providing_args=["follower", "unfollowed"])
