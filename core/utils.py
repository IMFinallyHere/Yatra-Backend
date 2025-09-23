from rest_framework.pagination import PageNumberPagination
from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, (
                AuthenticationFailed,
                NotAuthenticated)) and exc.detail == 'Authentication credentials were not provided.':
            response.data = {'non_field_errors': ['Authentication credentials were not provided']}
            response.status_code = exc.status_code if hasattr(exc, 'status_code') else 401
        elif isinstance(exc, PermissionDenied) and exc.detail == 'You do not have permission to perform this action.':
            response.data = {'non_field_errors': ['You do not have permission to perform this action.']}
            response.status_code = exc.status_code if hasattr(exc, 'status_code') else 403

    return response
