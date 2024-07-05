from django.shortcuts import render
from .models import User, componente, elementoCarrito, pedido, elementoPedido
from .forms import UserForm,componenteForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib import messages
from django.contrib.auth import logout
from .listas import MARCAS
from django.http import JsonResponse

def index(request):
    componentes = componente.objects.all()
    datos = {
        'componentes' : componentes
    }
    return render(request,'aplicacion/index.html',datos)

def login(request):
    return render(request,'registration/login.html')

def registrar(request):
    form=UserForm()
    datos={
       'form':form
    }
    if request.method=="POST":
       form=UserForm(data=request.POST)
       print(form.errors)
       if form.is_valid():
           form.save()
           usr=form.cleaned_data["username"]
           
           usuario = User.objects.get(username=usr)
           #permiso = Permission.objects.get(codename='add_persona') import Permission 
           #usuario.user_permissions.add(permiso)

           messages.success(request,"Nuevo usuario registrado")
           return redirect(to="login")
       
    return render(request,'registration/registrar.html',datos)

def cerrarSesion(request):
    logout(request)
    messages.info(request,'Sesión Cerrada')
    return redirect(to="index")

def listaProductos(request):
    componentes = componente.objects.all()
    datos = {
        'componentes' : componentes
    }

    print(request)
    

    return render(request,'aplicacion/listaproductos.html',datos)

def detalle(request,id):
    comp=get_object_or_404(componente,id=id)

    Marca = 'N/A'

    for marca in MARCAS:
        if marca[0] == comp.marca:
            Marca = marca[1]
    datos={
        "componente":comp,
        "marca":Marca,
    }

    

    if request.method=="POST":
        elemento, creado = elementoCarrito.objects.get_or_create(componente=comp,usuario=request.user)
        if not creado:
            elemento.cantidad += 1
        elemento.save()

        return redirect(to="carroCompras")

    return render(request,'aplicacion/detalle.html', datos)

def detallecomp(request,id):
    if id == '0':
        form=componenteForm()
        datos={
            'form':form
        }

        if request.method=="POST":
           form=componenteForm(data=request.POST)
           if form.is_valid():
            form.save()
            messages.success(request,'Componente creado')
            return redirect(to='listaProductos')
            

        return render(request,'aplicacion/detallecomponente.html', datos)
    else:
        comp=get_object_or_404(componente,id=id)
        form=componenteForm(instance=comp)
        datos={

           "componente":comp,
            'form':form
        }

        botonpresionado = None

        if request.method=="POST":
           botonpresionado = request.POST.get('boton')
           form=componenteForm(data=request.POST,instance=comp)
        if botonpresionado == 'eliminar':
            print("componente eliminado")
            comp.delete()
            messages.error(request,'Componente eliminado')
            return redirect(to='listaProductos')
        else:
            if form.is_valid():
                form.save()
                
                messages.info(request,'Componente modificado')
                return redirect(to='listaProductos')

        return render(request,'aplicacion/detallecomponente.html', datos)

def calcularPrecio(elementos):
    return sum(elemento.componente.precio * elemento.cantidad for elemento in elementos)
    

def carroCompras(request):
    elementos = elementoCarrito.objects.filter(usuario=request.user).select_related('componente')
    totalPrecio = calcularPrecio(elementos)

    datos = {
        'elementos': elementos,
        'totalPrecio': totalPrecio
    }

    if request.method == "POST":
        elemento_id = request.POST.get('elemento_id')
        elemento = get_object_or_404(elementoCarrito, id=elemento_id)
        accion = request.POST.get('accion')
        print(accion)

        if accion == 'actualizar':
            botonpresionado = request.POST.get('boton')
            print(botonpresionado)

            elemento.cantidad += int(botonpresionado)

            if elemento.cantidad <= 0:
                print("se pasó del mínimo")
                elemento.cantidad = 1

            elemento.save()

        elif accion == 'eliminar':
            print(elemento)
            elemento.delete()

        # Recalcular elementos y totalPrecio después de cualquier modificación
        elementos = elementoCarrito.objects.filter(usuario=request.user).select_related('componente')
        totalPrecio = calcularPrecio(elementos)
        print(totalPrecio, "Actualizado" if accion == 'actualizar' else "Eliminado")

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if accion == 'actualizar':
                return JsonResponse({'cantidad': elemento.cantidad, 'total_precio': totalPrecio})
            elif accion == 'eliminar':
                return JsonResponse({'success': True, 'total_precio': totalPrecio})
        else:
            return redirect(to='carroCompras')

    return render(request, 'aplicacion/carrodecompras.html', datos)

def metodoPago(request):
    elementos = elementoCarrito.objects.filter(usuario=request.user).select_related('componente')
    totalPrecio = calcularPrecio(elementos)

    for elemento in elementos:
        elemento.total_precio = elemento.componente.precio * elemento.cantidad

    datos = {
        'elementos': elementos,
        'totalPrecio': totalPrecio
    }

    return render(request,'aplicacion/metododepago.html',datos)

def pagoRealizado(request):

    elementos = elementoCarrito.objects.filter(usuario=request.user).select_related('componente')

    totalPrecio = calcularPrecio(elementos)

    for elemento in elementos:
        elemento.total_precio = elemento.componente.precio * elemento.cantidad

    datos = {
        'elementos': elementos,
        'totalPrecio': totalPrecio
    }

    if request.method == "POST":

        pedidocompra = pedido.objects.create(usuario=request.user, totalprecio=0)

        totalPrecio = 0

        for elemento in elementos:

            component = get_object_or_404(componente, id=elemento.componente.id)

            totalPrecio += elemento.cantidad * component.precio



            component.stock -= elemento.cantidad

            elementoPedido.objects.create(componente=component,pedido=pedidocompra,precio = component.precio,cantidad=elemento.cantidad)

            component.save()
            elemento.delete()

        pedidocompra.totalprecio = totalPrecio
        pedidocompra.save()

    return render(request,'aplicacion/pagorealizado.html',datos)

def usuario(request):
    pedidos = pedido.objects.filter(usuario = request.user)
    elementosPedidos = elementoPedido.objects.select_related('componente').all()

    datos={
        'pedidos':pedidos,
        'elementos':elementosPedidos
    }

    return render(request,'aplicacion/usuario.html',datos)

# Create your views here.