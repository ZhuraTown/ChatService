

class ApplicationException(Exception):
    @property
    def message(self) -> str:
        return 'An application error occurred'


class ToClientException(ApplicationException):
    ...