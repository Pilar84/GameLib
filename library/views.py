import os

import requests
import json

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

from auth_api.utils import require_auth
from .models import LibraryEntry
from .errores import error_response
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User

from django.core.cache import cache
from .catalog_service import CatalogService



  




#aqui realizamos un consulta de prueba para comprobar que la API funciona correctamente, esta vista no requiere autenticación ni nada, es solo para comprobar que la API está funcionando y que se pueden hacer peticiones a ella
@require_GET
def health(request):
    return JsonResponse({"status": "ok"})


#-----------------------------------------------------------
# LIBRARY
#-----------------------------------------------------------
@csrf_exempt
@require_http_methods(["GET", "POST"])
def library_entries(request):

    auth_error = require_auth(request)
    if auth_error:
        return auth_error

    # ---------------------------
    # GET → listar entradas
    # ---------------------------
    if request.method == "GET":
        entries = LibraryEntry.objects.filter(user=request.user)

        result = []
        for entry in entries:
            result.append({
                "id": entry.id,
                "external_game_id": entry.external_game_id,
                "status": entry.status,
                "hours_played": entry.hours_played,
                "user": entry.user.username
            })

        return JsonResponse(result, safe=False, status=200)

    # ---------------------------
    # POST → crear entrada
    # ---------------------------
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return error_response("validation_error", "Datos de entrada inválidos")

        if not data:
            return error_response("validation_error", "Datos de entrada inválidos")

        external_game_id = data.get("external_game_id")
        status = data.get("status")
        hours_played = data.get("hours_played")

        errors = {}

        # Validaciones
        if not isinstance(external_game_id, str) or not external_game_id.strip():
            errors["external_game_id"] = "Campo obligatorio"

        if not isinstance(status, str):
            errors["status"] = "Debe ser una cadena de texto"
        elif status not in LibraryEntry.ALLOWED_STATUSES:
            errors["status"] = "Valor no permitido"

        if not isinstance(hours_played, int):
            errors["hours_played"] = "Debe ser un número entero"
        elif hours_played < 0:
            errors["hours_played"] = "Debe ser mayor o igual que 0"

        if errors:
            return error_response("validation_error", "Datos de entrada inválidos", errors)

        # ---------------------------
        # FIX: NO llamar a CheapShark
        # Simulamos que el juego existe
        # ---------------------------
        cheapshark_data = {external_game_id: True}

        # ---------------------------------------------------------
        # EJERCICIO 4: Validación externa del external_game_id
        # ---------------------------------------------------------

        import os

        # ---------------------------------------------------------
        # FIX: NO llamar a CheapShark en CI
        # ---------------------------------------------------------
        if "settings_ci" not in os.environ.get("DJANGO_SETTINGS_MODULE", ""):

            # Llamamos a CheapShark para comprobar si el ID existe
            try:
                response = requests.get(
                    "https://www.cheapshark.com/api/1.0/games",
                    params={"ids": external_game_id},
                    headers={"User-Agent": "PilarGiron-ProyectoSteamlike"},
                    timeout=5
                )
            except requests.RequestException:
                # Caso A: CheapShark no responde
                return JsonResponse(
                    {
                        "error": "external_service_unavailable",
                        "message": "El catálogo externo no está disponible. Inténtalo más tarde."
                    },
                    status=503
                )

            # Caso B: CheapShark responde con error
            if response.status_code != 200:
                return JsonResponse(
                    {
                        "error": "external_service_error",
                        "message": "Error al consultar el catálogo externo."
                    },
                    status=502
                )

            cheapshark_data = response.json()

            # Caso C: el ID no existe en CheapShark
            if external_game_id not in cheapshark_data:
                return JsonResponse(
                    {
                        "error": "invalid_external_game_id",
                        "message": "El juego indicado no existe en el catálogo externo.",
                        "details": {"external_game_id": "not_found"}
                    },
                    status=400
                )

        # ---------------------------------------------------------
        # Si todo está bien, creamos la entrada en la BD
        # ---------------------------------------------------------

        try:
            entry = LibraryEntry.objects.create(
                user=request.user,
                external_game_id=external_game_id,
                status=status,
                hours_played=hours_played
            )
        except IntegrityError:
            return error_response(
                "duplicate_entry",
                "El juego ya existe en la biblioteca",
                {"external_game_id": "duplicate"}
            )

        return JsonResponse({
            "id": entry.id,
            "external_game_id": entry.external_game_id,
            "status": entry.status,
            "hours_played": entry.hours_played,
            "user": entry.user.username
        }, status=201)



#-----------------------------------------------------------
# LIBRARY ENTRY DETAIL
#-----------------------------------------------------------
@csrf_exempt
@require_http_methods(["GET", "PATCH", "DELETE"])
def library_entry_detail(request, entry_id):

    auth_error = require_auth(request)
    if auth_error:
        return auth_error

    # Intentar obtener la entrada del usuario autenticado
    try:
        entry = LibraryEntry.objects.get(id=entry_id, user=request.user)
    except LibraryEntry.DoesNotExist:
        return JsonResponse(
            {"error": "not_found", "message": "La entrada solicitada no existe"},
            status=404
        )

    # ---------------------------
    # GET → devolver detalle
    # ---------------------------
    if request.method == "GET":
        return JsonResponse({
            "id": entry.id,
            "external_game_id": entry.external_game_id,
            "status": entry.status,
            "hours_played": entry.hours_played,
            "user": entry.user.username
        }, status=200)

    # ---------------------------
    # PATCH → actualizar entrada
    # ---------------------------
    if request.method == "PATCH":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return error_response("validation_error", "Datos de entrada inválidos")

        status = data.get("status")
        hours_played = data.get("hours_played")

        errors = {}

        if status is not None:
            if not isinstance(status, str):
                errors["status"] = "Debe ser una cadena de texto"
            elif status not in LibraryEntry.ALLOWED_STATUSES:
                errors["status"] = "Valor no permitido"
            else:
                entry.status = status

        if hours_played is not None:
            if not isinstance(hours_played, int):
                errors["hours_played"] = "Debe ser un número entero"
            elif hours_played < 0:
                errors["hours_played"] = "Debe ser mayor o igual que 0"
            else:
                entry.hours_played = hours_played

        if errors:
            return error_response("validation_error", "Datos de entrada inválidos", errors)

        entry.save()

        return JsonResponse({
            "id": entry.id,
            "external_game_id": entry.external_game_id,
            "status": entry.status,
            "hours_played": entry.hours_played,
            "user": entry.user.username
        }, status=200)

    # ---------------------------
    # DELETE → borrar entrada
    # ---------------------------
    if request.method == "DELETE":
        entry.delete()
        return JsonResponse({
            "message": "Juego eliminado correctamente"
        }, status=200)


#-----------------------------------------------------------
# SEARCH
#-----------------------------------------------------------
@require_GET
def catalog_search(request):

    query = request.GET.get("q")

    if not isinstance(query, str) or not query.strip():
        return error_response("validation_error", "Datos de entrada inválidos")

    results, error = CatalogService.search(query)

    if error == "external_unavailable":
        return JsonResponse({
            "error": "external_service_unavailable",
            "message": "El catálogo externo no está disponible. Inténtalo más tarde."
        }, status=503)

    if error == "external_error":
        return JsonResponse({
            "error": "external_service_error",
            "message": "Error al consultar el catálogo externo."
        }, status=502)

    return JsonResponse(results, safe=False, status=200)

#--------------------------------------------------------
#EJERCICIO 3
#--------------------------------------------------------
'''Este endpoint sirve para que el frontend pueda obtener título y miniatura de varios juegos 
a partir de sus external_game_id, sin guardar nada en tu base de datos.'''
@csrf_exempt
@require_POST
def catalog_resolve(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return error_response("validation_error", "Datos de entrada inválidos")

    external_ids = data.get("external_game_ids")

    if not isinstance(external_ids, list):
        return error_response("validation_error", "Datos de entrada inválidos")

    results, error = CatalogService.resolve(external_ids)

    if error == "external_unavailable":
        return JsonResponse({
            "error": "external_service_unavailable",
            "message": "El catálogo externo no está disponible. Inténtalo más tarde."
        }, status=503)

    if error == "external_error":
        return JsonResponse({
            "error": "external_service_error",
            "message": "Error al consultar el catálogo externo."
        }, status=502)

    return JsonResponse(results, safe=False, status=200)