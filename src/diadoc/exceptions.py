class DiadocException(Exception):
    pass


class DiadocHTTPException(DiadocException):
    def __init__(self, code: int, message: str):
        super().__init__(code, message)
        self.code = code
        self.message = message
