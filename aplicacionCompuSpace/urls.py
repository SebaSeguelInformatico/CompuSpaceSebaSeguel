from django.urls import path
from .views import index,login,registrar,cerrarSesion,listaProductos,detallecomp

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('registrar/', registrar, name='registrar'),
    path('logout/', cerrarSesion, name='logout'),
    path('listaProductos/', listaProductos, name='listaProductos'),
    path('detallecomponente/<id>', detallecomp, name='detallecomponente'),
]