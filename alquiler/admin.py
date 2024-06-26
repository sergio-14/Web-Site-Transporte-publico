from django.contrib import admin

# Register your models here.
from .models import Categoria, Persona, RolSalida

admin.site.register(Categoria)
admin.site.register(Persona)
admin.site.register(RolSalida)
