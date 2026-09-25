import json
import requests
import os
import logging

logger = logging.getLogger(__name__)

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login 
from django.views.decorators.http import require_GET, require_http_methods
from django.db import IntegrityError
import json
from .utils import load_json
from .utils import require_auth
from django.contrib.auth import logout 

from library.models import LibraryEntry
from library.errores import error_response
from django.conf import settings
from .services import send_welcome_email    


# @csrf_exempt
# @require_POST
# def register(request):
#     #  aqui vamos aleer el JSON
#     data, error = load_json(request)
#     if error:
#         return error

#     # en este punto Extraemos los campos usuario y contraseña del JSON recibido
#     username = data.get("username")
#     password = data.get("password")

#     errors = {}

#     # Validamos los datos recibidos (que sean cadenas de texto y que la contraseña tenga al menos 8 caracteres)
#     if not isinstance(username, str) or not username.strip():
#         errors["username"] = "Campo obligatorio"

#     if not isinstance(password, str):
#         errors["password"] = "Debe ser una cadena de texto"
#     elif len(password) < 8:
#         errors["password"] = "Debe tener al menos 8 caracteres"

#     if errors:
#         return error_response(
#             "validation_error",
#             "Datos de entrada inválidos",
#             errors
#         )

#     # creamos el usuario en la base de datos (si el nombre de usuario ya existe, se captura la excepción y se devuelve un error)
#     try:
#         user = User.objects.create_user(
#             username=username,
#             password=password
#         )
#     except IntegrityError:
#         return error_response(
#             "validation_error",
#             "Datos de entrada inválidos",
#             {"username": "Ya está en uso"}
#         )

#     # devolvemos una respuesta con los datos del usuario creado (id y username)
#     return JsonResponse(
#         {
#             "id": user.id,
#             "username": user.username
#         },
#         status=201
#     )
    

@csrf_exempt
@require_POST
def register(request):
    # 1) Leer JSON
    data, error = load_json(request)
    if error:
        return error

    # 2) Extraer campos
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")  # ← NUEVO CAMPO

    errors = {}

    # 3) Validaciones
    if not isinstance(username, str) or not username.strip():
        errors["username"] = "Campo obligatorio"

    if not isinstance(password, str):
        errors["password"] = "Debe ser una cadena de texto"
    elif len(password) < 8:
        errors["password"] = "Debe tener al menos 8 caracteres"

    # Validación del email
    if not isinstance(email, str) or not email.strip():
        errors["email"] = "Campo obligatorio"
    elif "@" not in email:
        errors["email"] = "Formato inválido"

    if errors:
        return error_response(
            "validation_error",
            "Datos de entrada inválidos",
            errors
        )

    # 4) Crear usuario
    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email  # ← GUARDAR EMAIL
        )
    except IntegrityError:
        return error_response(
            "validation_error",
            "Datos de entrada inválidos",
            {"username": "Ya está en uso"}
        )

    # EJERCICIO 5 → Enviar email de bienvenida (NO afecta al registro si falla)
    send_welcome_email(user.email)
    
    
    # 5) Respuesta 201 con email incluido
    return JsonResponse(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email  # ← DEVOLVER EMAIL
        },
        status=201
    )



#aqui vamos a crear la vista para  login, que recibira un JSON con el nombre de usuario y la contraseña, y devolvera una respuesta con los datos del usuario logueado (id y username) si las credenciales son correctas, o un error si no lo son
@csrf_exempt
@require_POST
def login_view(request):
    #  aqui vamos a leer el JSON
    data, error = load_json(request)
    if error:
        return error

        
    # Extraemos los campos usuario y contraseña del JSON recibido
    username = data.get("username")
    password = data.get("password")

    # Validamos los datos recibidos (que sean cadenas de texto y que la contraseña tenga al menos 8 caracteres)
    if not isinstance(username, str) or not isinstance(password, str):
        return error_response(
            "validation_error",
            "Datos de entrada inválidos"
        )
    # Autenticamos al usuario con las credenciales recibidas
    user = authenticate(request, username=username, password=password)
    
   
    if user is None:
        return error_response(     
        "Credenciales incorrectas",
        "Credenciales incorrectas",
        status=401
    )

    #iniciar sesiion (django recuerda al usuario autenticado en la sesión)
    login(request, user)
    
    logger.info(f"login_view: login OK para usuario {username}")
    
    #respuesta correcta
    return JsonResponse(
        {
            "id": user.id,
            "username": user.username
        },
        status=200
    )

#------------------------------------------------------------------------------    
#EJERCICIO 6
#------------------------------------------------------------------------------    

# Vamos a implementar el logout
@csrf_exempt
@require_POST
def logout_view(request):
    logger.info("logout_view: cierre de sesión solicitado")
    # Da igual si está autenticado o no: siempre cerramos sesión
    logout(request)

    # 204 → No Content (respuesta vacía)
    return JsonResponse({}, status=204)




#aqui vamos a crear la vista para obtener los datos del usuario logueado, que recibira una petición GET y devolvera una respuesta con los datos del usuario logueado (id y username) si el usuario está autenticado, o un error si no lo está
@require_http_methods(["GET", "DELETE"])
def me(request):
    if not request.user.is_authenticated:
        return error_response(
            "unauthorized",
            "No autenticado",
            status=401
        )

    if request.method == "DELETE":
        user = request.user
        logout(request)
        user.delete()
        return JsonResponse({}, status=204)

    return JsonResponse(
        {
            "id": request.user.id,
            "username": request.user.username
        },
        status=200
    )

#--------------------------------------------------
#EJERCICIO 2
#--------------------------------------------------

@csrf_exempt
@require_POST

def change_password(request): 
    
    # Ejercicio 2 - Comprobar autenticacion
    auth_error = require_auth(request)
    if auth_error:
        return auth_error
        
    # Ejercicio 2 - Leer JSON
    data, error = load_json(request)
    if error:
        return error

        
    current_password = data.get("current_password")
    new_password = data.get("new_password")
    
    errors = {}
    
    #Validar campos obligatorios
    if not isinstance(current_password, str) or not current_password.strip():
        errors["current_password"] = "Campo obligatorio"
        
    if not isinstance(new_password, str) or not new_password.strip():
        errors["new_password"] = "Campo obligatorio"
    elif len(new_password) < 8:
        errors["new_password"] = "Debe tener al menos 8 caracteres"
        
    if errors:
        return error_response(
            "validation_error",
            "Datos de entrada inválidos",
            errors
        )
        
    # Comprobar contraseña actual 
    if not request.user.check_password(current_password):
        return error_response(
            "validation_error",
            "Contraseña actual incorrecta",
            {"current_password": "Contraseña actual incorrecta"}
        )   
        
    #Actuaizar contraseña
    request.user.set_password(new_password)
    request.user.save()
    
    #Respuesta correcta
    return JsonResponse ({"ok": True}, status=200)


#--------------------------------------------------
#ENVIO DE CORREO
#--------------------------------------------------
MAILEROO_URL = "https://smtp.maileroo.com/api/v2/emails"

@csrf_exempt
@require_POST
def send_email(request):
    # Leer JSON
    data, error = load_json(request)
    if error:
        return error

    to = data.get("to")
    subject = data.get("subject")
    text = data.get("text")

    errors = {}

    # Validaciones
    if not isinstance(to, str) or not to.strip():
        errors["to"] = "Campo obligatorio"

    if not isinstance(subject, str) or not subject.strip():
        errors["subject"] = "Campo obligatorio"

    if not isinstance(text, str) or not text.strip():
        errors["text"] = "Campo obligatorio"

    if errors:
        return error_response(
            "validation_error",
            "Datos de entrada inválidos",
            errors
        )

    # Cabeceras
    headers = {
        "Authorization": f"Bearer {os.getenv('MAILEROO_TOKEN')}",
        "Content-Type": "application/json",
    }

    # Payload
    payload = {
    "from": {"address": os.getenv("MAILEROO_FROM_ADDRESS")},
    "to": [{"address": data["to"]}],
    "subject": data["subject"],
    "plain": data["text"]
    }

    # Llamada a Maileroo
    try:
        r = requests.post(MAILEROO_URL, headers=headers, json=payload, timeout=5)
    except requests.RequestException:
        return JsonResponse(
            {"error": "external_service_unavailable"},
            status=503
        )

    # Si Maileroo responde con error
    if r.status_code >= 400:
        return JsonResponse(
        {
            "error": "external_service_error",
            "maileroo_status": r.status_code,
            "maileroo_response": r.text
        },
        status=502
    )
    # OK
    return JsonResponse({"ok": True}, status=200)

#--------------------------------------------------
# EJERCICIO 2 + EJERCICIO 3 (COMPLETO)
#--------------------------------------------------
@csrf_exempt
@require_POST
def debug_send_email(request):

    # 1) Solo disponible en DEBUG
    if not settings.DEBUG:
        return JsonResponse({"error": "not_available"}, status=404)

    # 2) Leer JSON
    data, error = load_json(request)
    if error:
        logger.warning(
            "debug_send_email: JSON inválido",
            extra={
                "action": "debug_send_email",
                "result": "validation_error"
            }
        )
        return error

    to = data.get("to")
    subject = data.get("subject")
    text = data.get("text")

    errors = {}

    # 3) Validaciones
    if not isinstance(to, str) or not to.strip():
        errors["to"] = "Campo obligatorio"

    if not isinstance(subject, str) or not subject.strip():
        errors["subject"] = "Campo obligatorio"

    if not isinstance(text, str) or not text.strip():
        errors["text"] = "Campo obligatorio"

    if errors:
        logger.warning(
            "debug_send_email: error de validación",
            extra={
                "action": "debug_send_email",
                "to": to,
                "result": "validation_error",
                "errors": errors
            }
        )
        return error_response("validation_error", "Datos de entrada inválidos", errors)

    # LOG: intento de envío
    logger.info(
        "debug_send_email: intento de envío",
        extra={
            "action": "debug_send_email",
            "to": to,
            "result": "attempt"
        }
    )

    # 4) Cabeceras
    headers = {
        "Authorization": f"Bearer {os.getenv('MAILEROO_TOKEN')}",
        "Content-Type": "application/json",
    }

    # 5) Payload
    payload = {
        "from": {"address": os.getenv("MAILEROO_FROM_ADDRESS")},
        "to": [{"address": to}],
        "subject": subject,
        "plain": text
    }

    # 6) Llamada a Maileroo
    try:
        r = requests.post(MAILEROO_URL, headers=headers, json=payload, timeout=5)
    except requests.RequestException as e:
        logger.error(
            "debug_send_email: fallo por timeout/red",
            extra={
                "action": "debug_send_email",
                "to": to,
                "result": "external_service_unavailable",
                "error": str(e)
            }
        )
        return JsonResponse({"error": "external_service_unavailable"}, status=503)

    # 7) Si Maileroo responde con error
    if r.status_code >= 400:
        logger.error(
            "debug_send_email: fallo por respuesta del proveedor",
            extra={
                "action": "debug_send_email",
                "to": to,
                "result": "external_service_error",
                "maileroo_status": r.status_code
            }
        )
        return JsonResponse(
            {
                "error": "external_service_error",
                "maileroo_status": r.status_code,
                "maileroo_response": r.text
            },
            status=502
        )

    # 8) OK
    logger.info(
        "debug_send_email: envío OK",
        extra={
            "action": "debug_send_email",
            "to": to,
            "result": "ok"
        }
    )

    return JsonResponse({"ok": True}, status=200)


