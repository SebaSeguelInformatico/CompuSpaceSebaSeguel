from django.urls import path
from .views import index,login,registrar,cerrarSesion,listaProductos,detallecomp,detalle,carroCompras,metodoPago,pagoRealizado,usuario

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('registrar/', registrar, name='registrar'),
    path('logout/', cerrarSesion, name='logout'),
    path('listaProductos/', listaProductos, name='listaProductos'),
    path('detallecomponente/<id>', detallecomp, name='detallecomponente'),
    path('detalle/<id>', detalle, name='detalle'),
    path('carroCompras/', carroCompras, name='carroCompras'),
    path('metodoPago/', metodoPago,name='metodoPago'),
    path('pagoRealizado/', pagoRealizado,name='pagoRealizado'),
    path('usuario/', usuario,name='usuario')
]