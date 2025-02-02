

def _success_response(data, message="Request successful"):
    """
    Generate a standardized success response.
    :param data: The actual response data.
    :param message: A success message.
    :return: JSON response.
    """
    return {
        'status': 'success',
        'message': message,
        'data': data
    }


def _error_response(error_message, status=400):
    """
    Generate a standardized error response.
    :param error_message: The error message to display.
    :param status: The HTTP status code (default is 400).
    :return: JSON response.
    """
    return {
        'status': 'error',
        'message': error_message,
        'code': status
    }
