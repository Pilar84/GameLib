from django.http import JsonResponse

def error_response(error, message, details=None, status=400):
    response = {
        "error": error,
        "message": message
    }

    if details is not None:
        response["details"] = details

    return JsonResponse(response, status=status)