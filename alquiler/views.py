from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistroForm
from .models import ventaboletos,Categoria

def home(request):
    return render(request, 'home.html')


    
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Usuario y/o contraseña incorrectos."
            return render(request, 'signin.html', {'error_message': error_message})
    return render(request, 'signin.html')

def agregar_registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'agregar_registro.html', {'form': form})

from django.utils.dateparse import parse_date
from django.db.models import Sum

def registro_list(request):
    registros = ventaboletos.objects.all()
    total_ganancias = 0

    # Obtener las fechas y categoría del formulario de entrada
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    categoria_id = request.GET.get('categoria')

    if fecha_inicio and fecha_fin:
        fecha_inicio = parse_date(fecha_inicio)
        fecha_fin = parse_date(fecha_fin)
        registros = registros.filter(fecha__range=[fecha_inicio, fecha_fin])

    if categoria_id:
        registros = registros.filter(persona__categoria_id=categoria_id)

    total_ganancias = registros.aggregate(Sum('total'))['total__sum'] or 0

    categorias = Categoria.objects.all()

    return render(request, 'registro_list.html', {
        'registros': registros,
        'total_ganancias': total_ganancias,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'categoria_id': categoria_id,
        'categorias': categorias,
    })

from django.http import JsonResponse
from .models import Persona

def get_asientos_disponibles(request):
    persona_id = request.GET.get('persona_id')
    persona = Persona.objects.get(id=persona_id)
    categoria = persona.categoria
    asientos_ocupados = ventaboletos.objects.filter(persona__categoria=categoria).values_list('asiento', flat=True)
    asientos_disponibles = [i for i in range(1, categoria.asientos + 1) if i not in asientos_ocupados]
    return JsonResponse({'asientos_disponibles': asientos_disponibles, 'asientos_ocupados': list(asientos_ocupados)})


from .forms import RolSalidaForm

def agregar_rol_salida(request):
    if request.method == 'POST':
        form = RolSalidaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirige a la lista de roles de salida después de agregar uno nuevo
    else:
        form = RolSalidaForm()
    return render(request, 'agregar_rol_salida.html', {'form': form})

# views.py
from .models import RolSalida
from datetime import datetime, date, timedelta

def lista_rol_salida(request):

    categorias = Categoria.objects.all()

   
    categoria_filtrar = request.GET.get('categoria', None)

    now = datetime.now()
    start_of_day = datetime.combine(date.today(), datetime.min.time())
    end_of_day = datetime.combine(date.today(), datetime.max.time())

    
    roles_salida = RolSalida.objects.filter(
        persona__categoria__categoria=categoria_filtrar,
        hora_inicio__gte=start_of_day.time(),
        hora_inicio__lte=end_of_day.time(),
        status='pendiente'
    )

    return render(request, 'lista_rol_salida.html', {'roles_salida': roles_salida, 'categorias': categorias})

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

def cambiar_estado_rol_salida(request, rol_id):
    rol = get_object_or_404(RolSalida, id=rol_id)
    if rol.status == 'pendiente':
        rol.status = 'realizado'
        rol.save()
    return HttpResponseRedirect(reverse('lista_rol_salida'))