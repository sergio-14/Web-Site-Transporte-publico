#transporte que me permita vender boletos por asiento  asignarle roles de salia a 
#los vehiculos clasificar vehiculos por categoria y un registro de ganancias total  

from django.db import models
from django.conf import settings

class Categoria(models.Model):
    categoria = models.CharField(max_length=255)
    asientos = models.PositiveIntegerField()

    def __str__(self):
        return self.categoria

    class Meta:
        verbose_name_plural = "Categorías"

class Persona(models.Model):
    imagen = models.ImageField(upload_to='imagenes/usuarios', verbose_name='Imagen', null=True, blank=True)
    dni = models.CharField(verbose_name='DNI', max_length=50, unique=True, help_text='Documento Nacional de Identidad')
    fecha_nacimiento = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoría')
    telefono = models.CharField(verbose_name='Teléfono', max_length=20, blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Usuario relacionado')
    estado = models.BooleanField(default=True)
    #turno = models.ForeignKey(Turno, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Turno')


    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = "Personas"
        ordering = ['user']
        
class Turno(models.Model):
    nombre = models.CharField(max_length=50)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    def __str__(self):
        return self.nombre
    
class RolSalida(models.Model):
    STATUS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('realizado', 'Realizado'),
    ]

    nombre = models.CharField(max_length=50, verbose_name='Agregar Turno o Descripcion')
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, verbose_name='Asignar Personal o Chofer')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendiente', verbose_name='Estado')

class ventaboletos(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, verbose_name='Chofer o Persona a Cargo')
    cliente = models.CharField(max_length=150, verbose_name='Cliente')
    detalle = models.TextField(verbose_name='Detalle', blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    boleto = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    asiento = models.PositiveIntegerField(verbose_name='Número de Asiento')

    def __str__(self):
        return f"{self.cliente} - Asiento {self.asiento}"

    class Meta:
        verbose_name_plural = "Registros"
        ordering = ['fecha']
        unique_together = ('persona', 'asiento')
        
        

class Registro(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, verbose_name='Persona relacionada')
    cliente = models.CharField(max_length=150, verbose_name='Cliente')
    detalle = models.TextField(verbose_name='Detalle', blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    boleto = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.cliente

    class Meta:
        verbose_name_plural = "Registros"
        ordering = ['fecha']