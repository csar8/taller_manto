from django import forms
from .models import UsuariosGenerales

class UsuariosForm(forms.ModelForm):
    contraseña = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    confirmar_contraseña = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)
    correo_electronico = forms.EmailField(label='Correo Electrónico')
    class Meta:
        model = UsuariosGenerales
        fields = ['nombre_de_usuario', 'nombre', 'apellido_paterno', 'apellido_materno', 'correo_electronico', 'telefono', 'contraseña', 'confirmar_contraseña']
#-----------------------------------------------------------------------
from .models import SalidaArticulo
from .models import EntradaArticulo
from .models import Inventario
class EntradaArticuloForm(forms.ModelForm):
    class Meta:
        model = EntradaArticulo
        fields = ['nombre_de_articulo', 'categoria', 'unidad_de_medida', 'cantidad_disponible']
class SalidaArticuloForm(forms.ModelForm):
    nombre_de_articulo = forms.ModelChoiceField(queryset=Inventario.objects.all(), label="Artículo de Entrada")
    class Meta:
        model = SalidaArticulo
        fields = ['nombre_de_articulo','numero_orden', 'unidad', 'cantidad', 'departamento' ]
#---------------------------------------------------------------------------
from .models import OrdenSalida
class OrdenSalidaForm(forms.ModelForm):
    class Meta:
        model = OrdenSalida
        fields = ['nombre_de_articulo', 'numero_orden', 'unidad', 'cantidad']
#-----------------------------------------------------------------------------
from .models import Factura
class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['clave_de_registro', 'numero_de_folio', 'concepto', 'fecha_de_factura', 'archivo']
        widgets = {
            'fecha_de_factura': forms.DateInput(attrs={'type': 'date'})
        }
#-----------------------------------------------------------------------------
