import json
from django.http import JsonResponse
from library.errores import error_response



def load_json(request):
    try:
        data = json.loads(request.body)
        if not data:
            raise ValueError
        return data, None
    except:
        return None, error_response("validation_error", "Datos de entrada inválidos")



#funcion de autenticacion de usuarios
def require_auth(request):
    if not request.user.is_authenticated:
        return error_response(
            "unauthorized",
            "No autenticado",
            status=401
        )
    return None
    