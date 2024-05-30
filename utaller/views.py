from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect  # Agregamos la importación de redirect
from .models import UsuariosGenerales
from django.contrib import messages
from .forms import UsuariosForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def login(request):
    if request.method == 'POST':
        nombre_de_usuario = request.POST.get('nombre_de_usuario')
        contraseña = request.POST.get('contraseña')
        # Verificar si el usuario existe en la base de datos
        try:
            usuario = UsuariosGenerales.objects.get(nombre_de_usuario=nombre_de_usuario)
            if usuario.check_password(contraseña):
                if usuario.activo:
                    request.session['usuario_id'] = usuario.id
                    return redirect('index') 
                else:
                    return redirect('aviso')
            else:
                messages.error(request, 'Contraseña incorrecta.')
        except UsuariosGenerales.DoesNotExist:
            messages.error(request, 'El usuario no existe.')
    return render(request, 'login.html')
#----------------------------------------------------------------

def registro(request):
    if request.method == 'POST':  # Verifica si se ha enviado un formulario
        form = UsuariosForm(request.POST)  # Inicializa el formulario con los datos recibidos
        if form.is_valid():  # Valida el formulario
            nombre_de_usuario = form.cleaned_data['nombre_de_usuario']
            if User.objects.filter(username=nombre_de_usuario).exists():
                messages.error(request, '¡El usuario ya existe! Por favor, elige otro nombre de usuario.')
            else:
                usuario = form.save(commit=False)
                usuario.set_password(form.cleaned_data['contraseña'])
                usuario.save()
                messages.success(request, '¡Usuario creado con éxito!')
                return redirect('registro')
        else:
            messages.error(request, '¡Error en el formulario! Por favor, corrige los errores e intenta nuevamente.')  # Muestra un mensaje de error
    else:
        form = UsuariosForm()  # Crea un formulario vacío si la solicitud no es de tipo POST
    return render(request, 'registro.html', {'form': form})  # Renderiza la plantilla con el formulario

#------------------------------------------------------------------

from .models import EntradaArticulo, SalidaArticulo, Inventario
from .forms import SalidaArticuloForm
from .forms import EntradaArticuloForm
from django.db.models import Q

def gestionex(request):
    query = request.GET.get('q')
    
    if query:
        inventario = Inventario.objects.filter(
            Q(nombre__icontains=query) |
            Q(categoria__icontains=query) |
            Q(unidad_de_medida__icontains=query)
        ).order_by('-ultima_modificacion')
    else:
        inventario = Inventario.objects.all().order_by('-ultima_modificacion')
    
    return render(request, 'gestionex.html', {'inventario': inventario, 'search_query': query})
#------------------------------------------------------------------
from django.db.models import Q

def entrada(request):
    query = request.GET.get('q')
    entradas = EntradaArticulo.objects.all().order_by('-fecha_y_hora')  # Ordenar por fecha y hora en orden descendente
    if query:
        entradas = entradas.filter(
            Q(nombre_de_articulo__icontains=query) |
            Q(categoria__icontains=query) |
            Q(unidad_de_medida__icontains=query)
        )
    if request.method == 'POST':
        form = EntradaArticuloForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artículo agregado con éxito')
            return redirect('entrada')
        else:
            messages.error(request, 'Error al agregar el artículo. Por favor, verifica el formulario.')
    else:
        form = EntradaArticuloForm()
    return render(request, 'entrada.html', {'form': form, 'entradas': entradas, 'search_query': query})

#------------------------------------------------------------------

def salida(request):
    query = request.GET.get('q')
    salidas = SalidaArticulo.objects.all().order_by('-fecha_y_hora_salida')
    if query:
        salidas = salidas.filter(
            Q(nombre_de_articulo__nombre__icontains=query) |  # Buscar en el nombre del artículo
            Q(numero_orden__icontains=query) |                # Buscar en el número de orden
            Q(unidad__icontains=query) |                      # Buscar en la unidad
            Q(departamento__icontains=query)
        )
    if request.method == 'POST':
        form = SalidaArticuloForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Salida registrada con éxito.')
                return redirect('salida')
            except ValueError as e:
                form.add_error(None, str(e))
                messages.error(request, f'Error: {e}')
        else:
            messages.error(request, 'Formulario no válido.')
    else:
        form = SalidaArticuloForm()
    return render(request, 'salida.html', {'salidas': salidas, 'form': form})

#------------------------------------------------------------------

from .models import Inventario, OrdenSalida
from .forms import OrdenSalidaForm
from django.utils import timezone

def orden_salida(request):
    query = request.GET.get('q')
    ordenes_salida = OrdenSalida.objects.all().order_by('-fecha_y_hora')
    if query:
        ordenes_salida = ordenes_salida.filter(
            Q(nombre_de_articulo__nombre__icontains=query) |
            Q(numero_orden__icontains=query) |
            Q(unidad__icontains=query)
        )
    if request.method == "POST":
        form = OrdenSalidaForm(request.POST)
        if form.is_valid():
            orden_salida = form.save(commit=False)
            inventario = orden_salida.nombre_de_articulo
            if inventario.cantidad_disponible < orden_salida.cantidad:
                messages.error(request, "No hay suficiente cantidad en inventario.")
                return render(request, 'orden_salida.html', {'form': form, 'ordenes_salida': ordenes_salida})
            orden_salida.save()
            messages.success(request, 'La orden de salida se realizó correctamente')
            return redirect('orden_salida')
    else:
        form = OrdenSalidaForm()
    return render(request, 'orden_salida.html', {'form': form, 'ordenes_salida': ordenes_salida})

#------------------------------------------------------------------------

from django.shortcuts import render, redirect, get_object_or_404
from .models import Factura
from .forms import FacturaForm

def facturas(request):
    query = request.GET.get('q')
    facturas = Factura.objects.all()
    if query:
        facturas = facturas.filter(
            Q(clave_de_registro__icontains=query) |
            Q(numero_de_folio__icontains=query) |
            Q(concepto__icontains=query)
        )
    if request.method == 'POST':
        if 'delete' in request.POST:
            factura_id = request.POST.get('factura_id')
            factura = get_object_or_404(Factura, id=factura_id)
            factura.delete()
            messages.success(request, '¡La factura se eliminó con éxito!')
            return redirect('facturas')

        else:
            form = FacturaForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, '¡La factura se añadió con éxito!')
                return redirect('facturas')
    else:
        form = FacturaForm()

    facturas = Factura.objects.all().order_by('-fecha_de_factura')
    return render(request, 'facturas.html', {'form': form, 'facturas': facturas})

#------------------------------------------------------------------------


def reportes(request):
    return render(request, 'reportes.html')
def index(request):
    return render(request, 'index.html')
def aviso(request):
    return render (request, 'aviso.html')
def Header(request):
    return render(request, 'Header.html')


def Iniciar_Sesión(request):
    logout(request)
    return redirect('login')
def Cerrar_Sesión(request):
    logout(request)
    return redirect('login')