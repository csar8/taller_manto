from django.contrib import admin
from .models import UsuariosGenerales
from .models import EntradaArticulo
from .models import SalidaArticulo
from .models import Inventario
from .models import OrdenSalida
from .models import Factura


class UsuariosAdmin(admin.ModelAdmin):
        list_display = ['nombre_de_usuario', 'nombre', 'apellido_paterno', 'apellido_materno', 'correo_electronico', 'telefono']
admin.site.register(UsuariosGenerales, UsuariosAdmin)

class InventarioAdmin(admin.ModelAdmin):
        list_display = ['nombre', 'categoria', 'unidad_de_medida', 'cantidad_disponible']
        search_fields = ['nombre', 'categoria', 'unidad_de_medida']  
admin.site.register(Inventario, InventarioAdmin)

class EntradaArticuloAdmin(admin.ModelAdmin):
        list_display = ['nombre_de_articulo', 'categoria', 'unidad_de_medida', 'cantidad_disponible', 'fecha_y_hora']
        search_fields = ['nombre_de_articulo', 'categoria', 'unidad_de_medida'] 
        list_filter = ['categoria', 'unidad_de_medida']
admin.site.register(EntradaArticulo, EntradaArticuloAdmin)

class SalidaArticuloAdmin(admin.ModelAdmin):
        list_display = [ 'nombre_de_articulo', 'numero_orden', 'unidad', 'cantidad', 'fecha_y_hora_salida', 'departamento']
        search_fields = ['nombre_de_articulo', 'numero_orden', 'unidad', 'departamento' ]  
admin.site.register(SalidaArticulo, SalidaArticuloAdmin)

class OrdenSalidaAdmin(admin.ModelAdmin):
        list_display = [ 'nombre_de_articulo', 'numero_orden', 'unidad', 'cantidad', 'fecha_y_hora']
        search_fields = ['nombre_de_articulo__nombre', 'numero_orden', 'unidad']
admin.site.register(OrdenSalida, OrdenSalidaAdmin)

class FacturaAdmin(admin.ModelAdmin):
        list_display = [ 'clave_de_registro', 'numero_de_folio', 'concepto', 'fecha_de_factura', 'archivo']
        search_fields = ['clave_de_registro', 'numero_de_folio', 'concepto']
admin.site.register(Factura, FacturaAdmin)

from .models import Reportes

class ReporteAdmin(admin.ModelAdmin):
        list_display = [ 'clave_de_registro', 'numero_de_folio', 'concepto', 'fecha_de_reportes', 'archivo']
        search_fields = ['clave_de_registro', 'numero_de_folio', 'concepto']

admin.site.register(Reportes, ReporteAdmin)



