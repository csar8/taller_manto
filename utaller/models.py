from django.db import models
from django.contrib import admin
import bcrypt
from django_otp.models import SideChannelDevice
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UsuariosGenerales(models.Model):
    nombre_de_usuario = models.CharField(max_length=150, unique=True)
    nombre= models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100) 
    apellido_materno = models.CharField(max_length=100)
    correo_electronico = models.EmailField(unique=True)  # Nuevo campo para el correo electrónico
    telefono = models.PositiveIntegerField()
    contraseña_hash = models.CharField(max_length=128)  
    activo = models.BooleanField(default=False)  # Por defecto, el usuario estará inactivo
    otp_secret = models.CharField(max_length=16, blank=True, null=True)
    otp_enabled = models.BooleanField(default=False)

    def enable_otp(self):
        device = SideChannelDevice.objects.create(user=self)
        self.otp_secret = device.bin_key
        self.otp_enabled = True
        self.save()

    def disable_otp(self):
        self.otp_secret = None
        self.otp_enabled = False
        self.save()

    def __str__(self):
        return self.nombre

    def set_password(self, raw_password):
        # Genera el hash de la contraseña utilizando bcrypt
        self.contraseña_hash = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, raw_password):
        # Verifica si la contraseña proporcionada coincide con la contraseña almacenada
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.contraseña_hash.encode('utf-8'))


@receiver(post_save, sender=User)
def set_user_inactive(sender, instance, created, **kwargs):
    if created:
        instance.activo = False
        instance.save()

#--------------------------------------------------------------------
CATEGORIAS = [
    ('refacciones', 'Refacciones'),
    ('herramientas', 'Herramientas'),
    ('aceites', 'Aceites'),
    ('filtros', 'Filtros'),
    ('llantas', 'Llantas'),
    ('combustible', 'Combustible'),
]

# Definir las opciones para las unidades de medida
UNIDADES_DE_MEDIDA = [
    ('pieza', 'Pieza'),
    ('metro', 'Metro'),
    ('gramo', 'Gramo'),
    ('kilogramo', 'Kilogramo'),
    ('litro', 'Litro'),
]

DEPARTAMENTOS = [
    ('limpia_pública',  'Limpia Pública'),
    ('maquinaria_pesada',  'Maquinaria Pesada'),
    ('obras_públicas',  'Obras Públicas'),
    ('ornatos', 'Ornatos'),
    ('policía_municipal', 'Policía Municipal'),
    ('presidencia', 'Presidencia'),
    ('protección_civil', 'Protección Civil'),
    ('recursos_humanos', 'Recursos Humanos'),
    ('infraestructura_urbana', 'Infraestructura Urbana'),
    ('gobierno', 'Gobierno'),
    ('dirección_de_ingresos', 'Dirección De Ingresos'),
    ('dirección_de_gobernación', 'Dirección De Gobernación'),
    ('dif_municipal', 'Dif Municipal'),
    ('desarrollo_urbano_y_medio_ambiente', 'Desarrollo Urbano Y Medio Ambiente'),
    ('comunicación_social', 'Comunicación Social'),
    ('alumbrado_público', 'Alumbrado Público'),
    ('basurero_municipal', 'Basurero Municipal'),
    ('atención_y_participación_ciudadana', 'Atención Y Participación Ciudadana'),
    ('agencia_municipal_de_mundo_nuevo', 'Agencia Municipal De Mundo Nuevo'),
    ('acción_social', 'Acción Social'),
]

from django.utils import timezone

class Inventario(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    unidad_de_medida = models.CharField(max_length=20, choices=UNIDADES_DE_MEDIDA)
    cantidad_disponible = models.PositiveIntegerField(default=0)
    ultima_modificacion = models.DateTimeField(default=timezone.now)  # Nuevo campo para la última modificación

    def __str__(self):
        return self.nombre

#---------------------------------------------------------------------------------------
class EntradaArticulo(models.Model):
    nombre_de_articulo = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    unidad_de_medida = models.CharField(max_length=20, choices=UNIDADES_DE_MEDIDA)
    cantidad_disponible = models.PositiveIntegerField()
    fecha_y_hora = models.DateTimeField(default=timezone.now)  # Asigna un valor por defecto

    def __str__(self):
        return f"{self.nombre_de_articulo} - {self.fecha_y_hora.strftime}"
    
    def save(self, *args, **kwargs):
        inventario, created = Inventario.objects.get_or_create(
            nombre=self.nombre_de_articulo, categoria=self.categoria, unidad_de_medida=self.unidad_de_medida)
        inventario.cantidad_disponible += self.cantidad_disponible
        inventario.ultima_modificacion = timezone.now()  # Actualizar la fecha y hora de la última modificación
        inventario.save()
        super().save(*args, **kwargs)

#---------------------------------------------------------------------------------------

class SalidaArticulo(models.Model):
    nombre_de_articulo = models.ForeignKey(Inventario, on_delete=models.CASCADE, blank=True,null=True)
    numero_orden = models.CharField(max_length=100)
    unidad = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    departamento = models.CharField(max_length=100, choices=DEPARTAMENTOS)
    fecha_y_hora_salida = models.DateTimeField(default=timezone.now)  # Asigna un valor por defecto

    def __str__(self):
        return f"Orden {self.numero_orden} - {self.fecha_y_hora_salida.strftime}"
    
    def save(self, *args, **kwargs):
        Inventario = self.nombre_de_articulo  # Aquí es donde hacemos el ajuste
        if Inventario.cantidad_disponible  < self.cantidad:
            raise ValueError("No hay suficiente cantidad en inventario.")
        Inventario.cantidad_disponible -= self.cantidad
        Inventario.ultima_modificacion = timezone.now()  # Actualizar la fecha y hora de la última modificación
        Inventario.save()
        super().save(*args, **kwargs)
        
#---------------------------------------------------------------------------------------

class OrdenSalida(models.Model):
    nombre_de_articulo = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    numero_orden = models.CharField(max_length=100)
    unidad = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    fecha_y_hora = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Orden {self.numero_orden} - {self.fecha_y_hora.strftime}"
    def save(self, *args, **kwargs):
        inventario = self.nombre_de_articulo
        if inventario.cantidad_disponible < self.cantidad:
            raise ValueError("No hay suficiente cantidad en inventario.")
        super().save(*args, **kwargs)


#---------------------------------------------------------------------------------------
class Factura(models.Model):
    clave_de_registro = models.CharField(max_length=100)
    numero_de_folio = models.CharField(max_length=100)
    concepto = models.CharField(max_length=100)
    fecha_de_factura = models.DateField()
    archivo = models.FileField(upload_to='facturas/')

    def __str__(self):
        return f'Factura {self.numero_de_folio} - {self.concepto}'
    
#---------------------------------------------------------------------------------------
class Reportes(models.Model):
    clave_de_registro = models.CharField(max_length=100)
    numero_de_folio = models.CharField(max_length=100)
    concepto = models.CharField(max_length=100)
    fecha_de_reportes = models.DateField()
    archivo = models.FileField(upload_to='reportes/')

    def __str__(self):
        return f'Reportes {self.numero_de_folio} - {self.concepto}'