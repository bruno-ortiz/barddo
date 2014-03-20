from core.exceptions import BarddoError


class UserNotProvided(BarddoError):
    """
    When views that need an user don't receive one
    """
    pass