from django.shortcuts import render
from .models import User, componente
from .forms import UserForm,componenteForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib import messages
from django.contrib.auth import logout
from .listas import MARCAS

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


# Create your views here.