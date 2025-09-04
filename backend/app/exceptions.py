

class BaseAppException(Exception):
    pass


class ProductNotFoundError(BaseAppException):
    pass


class OrderNotFoundError(BaseAppException):
    pass


class DatabaseError(BaseAppException):
    pass


class ValidationError(BaseAppException):
    pass
