from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that automatically catches all exceptions
    and returns appropriate status codes with error messages.

    - DRF APIExceptions (ParseError, NotFound, etc.) keep their status codes
    - Unhandled exceptions return 500 with error message
    """
    # Call REST framework's default exception handler first
    # This handles DRF APIExceptions (ParseError, NotFound, PermissionDenied, etc.)
    response = exception_handler(exc, context)

    # If the exception is not handled by DRF's default handler
    # (i.e., it's not a DRF APIException), handle it ourselves
    if response is None:
        # Log the exception if needed (you can add logging here)
        error_message = str(exc)

        # Return a 500 response with the error message
        return Response(
            {"detail": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # DRF already handled it with appropriate status code
    # Optionally normalize the error format if needed
    if response is not None and isinstance(response.data, dict):
        # Ensure consistent error format - use "error" key if "detail" exists
        if "detail" in response.data:
            response.data = {"detail": response.data["detail"]}

    return response
