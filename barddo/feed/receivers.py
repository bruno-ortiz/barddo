from django.dispatch import receiver

from accounts.models import BarddoUser
from accounts.signals import account_created
from core.models import Collection
from feed.models import CollectionSubscribeAction
from follow.signals import start_follow, stop_follow
from models import UserFeed, JoinAction, FollowAction, UnFollowAction


def register():
    pass


@receiver(account_created)
def handle_user_created(sender, **kwargs):
    """
    Dispatched everytime a new user is created
    """
    user = kwargs.get("user")
    UserFeed.objects.create(user=user, action=JoinAction.objects.create())


@receiver(start_follow)
def handle_follow(sender, **kwargs):
    """
    Dispatched everytime a user start to follow another user
    """
    follower = kwargs.get("follower")
    followed = kwargs.get("followed")
    if isinstance(followed, BarddoUser):
        UserFeed.objects.create(user=follower, action=FollowAction.objects.create(target=followed))
    elif isinstance(followed, Collection):
        UserFeed.objects.create(user=follower, action=CollectionSubscribeAction.objects.create(target=followed))


@receiver(stop_follow)
def handle_unfollow(sender, **kwargs):
    """
    Dispatched everytime a user stop follow another user
    """
    follower = kwargs.get("follower")
    followed = kwargs.get("unfollowed")
    if isinstance(followed, BarddoUser):
        UserFeed.objects.create(user=follower, action=UnFollowAction.objects.create(target=followed))
