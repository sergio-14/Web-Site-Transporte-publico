"""
URL configuration for administrador project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from alquiler import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('agregar_registro', views.agregar_registro, name='agregar_registro'),
    path('registros_list', views.registro_list, name='registro_list'),
    path('get_asientos_disponibles/', views.get_asientos_disponibles, name='get_asientos_disponibles'),
    path('agregar-rol-salida/', views.agregar_rol_salida, name='agregar_rol_salida'),
    path('lista-rol-salida/', views.lista_rol_salida, name='lista_rol_salida'),
    path('cambiar_estado_rol_salida/<int:rol_id>/', views.cambiar_estado_rol_salida, name='cambiar_estado_rol_salida'),
    #logueamiento
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)