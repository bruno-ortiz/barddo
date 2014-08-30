from core.exceptions import ChangeOnObjectNotOwnedError


def validate_work_owner(user, work):
    if not work.is_owner(user):
        raise ChangeOnObjectNotOwnedError()