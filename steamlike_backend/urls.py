from django.contrib import admin
from django.urls import path, include
from auth_api.views import me 
from auth_api.views import change_password
from library.views import (
    health,
    library_entries,    
    library_entry_detail,
    catalog_search,
    catalog_resolve
)


urlpatterns = [

    path("admin/", admin.site.urls),
    path("api/health/", health),

    # LISTADO (GET) y CREAR (POST)
    path("api/library/entries/", library_entries),

    # DETALLE (GET) y ACTUALIZAR (PATCH)
    path("api/library/entries/<int:entry_id>/", library_entry_detail),
    
    #aqui añadimos la ruta para el registro de usuarios
    path("api/auth/", include("auth_api.urls")),
    
    path("api/users/me/", me),
    
    path("api/users/me/password/", change_password),
    
    path("api/catalog/search/", catalog_search),

    path("api/catalog/resolve/", catalog_resolve),
    
]
