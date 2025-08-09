import typing


class ResponseException(Exception):
    def __init__(self, status_code: int, detail: typing.AnyStr):
        self.status_code = status_code
        self.detail = detail


class UnauthorizedAccessException(ResponseException):
    def __init__(self, detail="Unauthorized access."):
        super().__init__(status_code=401, detail=detail)


class ForbiddenAccessException(ResponseException):
    def __init__(self, detail="Forbidden access."):
        super().__init__(status_code=403, detail=detail)


class ResourceNotFoundException(ResponseException):
    def __init__(self, detail="Resource not found."):
        super().__init__(status_code=404, detail=detail)


class ValidationException(ResponseException):
    def __init__(self, detail="Validation error."):
        super().__init__(status_code=422, detail=detail)


class DataAlreadyExistsException(ResponseException):
    def __init__(self, detail="The data already exists."):
        super().__init__(status_code=409, detail=detail)
        self.detail = detail


class InvalidDataException(ResponseException):
    def __init__(self, detail="Data is invalid."):
        super().__init__(status_code=400, detail=detail)
        self.detail = detail


class FailureSaveDataException(ResponseException):
    def __init__(self, detail="Could not save data."):
        super().__init__(status_code=400, detail=detail)
        self.detail = detail


class NotFoundException(ResponseException):
    def __init__(self, detail="Data not found."):
        super().__init__(status_code=404, detail=detail)
        self.detail = detail


class BadRequestException(ResponseException):
    def __init__(self, detail="Data not found."):
        super().__init__(status_code=400, detail=detail)
        self.detail = detail


class InvalidRequestException(ResponseException):
    def __init__(self, detail="Invalid request."):
        super().__init__(status_code=409, detail=detail)
        self.detail = detail
