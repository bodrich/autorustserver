class UpdaterException(Exception):
    pass


class NotFoundBuildIdException(UpdaterException):
    pass


class RequestException(UpdaterException):
    pass


class ShellCommandErrorException(Exception):
    pass

