from fastapi import HTTPException, status


class AppException(Exception):
    """Base application exception"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationException(AppException):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class AuthorizationException(AppException):
    """Raised when authorization fails"""
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class NotFoundException(AppException):
    """Raised when resource is not found"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class ValidationException(AppException):
    """Raised when validation fails"""
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY)


class ConflictException(AppException):
    """Raised when resource already exists"""
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, status.HTTP_409_CONFLICT)


class InsufficientFundsException(AppException):
    """Raised when wallet has insufficient funds"""
    def __init__(self, message: str = "Insufficient funds in wallet"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class AuctionException(AppException):
    """Raised for auction-related errors"""
    def __init__(self, message: str = "Auction operation failed"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class BidException(AppException):
    """Raised for bid-related errors"""
    def __init__(self, message: str = "Bid operation failed"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class PaymentException(AppException):
    """Raised for payment-related errors"""
    def __init__(self, message: str = "Payment operation failed"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


def to_http_exception(exc: AppException) -> HTTPException:
    """Convert AppException to HTTPException"""
    return HTTPException(
        status_code=exc.status_code,
        detail=exc.message
    )
