from django.urls import path
from .views import register, login_view, logout_view 
from .views import send_email 
from .views import debug_send_email


urlpatterns = [
    path("register/", register),
    path("login/", login_view), 
    path("logout/", logout_view),
    path("send-email/", send_email),
   
]

