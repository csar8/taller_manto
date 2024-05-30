from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[ 
    path ('',views.gestionex, name = 'index',),
    path ('Header/',views.Header, name = 'Header',),

    path ('gestionex/', views.gestionex, name='gestionex',),    
    path('reportes/', views.reportes, name='reportes'),
    path ('entrada/', views.entrada, name='entrada',),
    path ('salida/', views.salida, name='salida',),
    path('orden_salida/', views.orden_salida, name='orden_salida'),
    path ('facturas/', views.facturas, name='facturas',),

    path ('login/', views.login, name='login',),
    path ('registro/', views.registro, name='registro',),
    path ('aviso/', views.aviso, name='aviso',),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)