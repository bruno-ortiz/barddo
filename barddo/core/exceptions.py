class BarddoError(Exception):
    """
    Basic project exception
    """
    pass


class InvalidFileUploadError(BarddoError):
    """
    When the user is trying to upload an invalid type file
    """
    pass


class ChangeOnObjectNotOwnedError(BarddoError):
    """
    When the user is trying to manage a collection of work and don't owns it
    """
    pass