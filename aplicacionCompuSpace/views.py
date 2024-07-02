from django.shortcuts import render
from .models import User, componente
from .forms import UserForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib import messages
from django.contrib.auth import logout

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

def detallecomp(request,idcomp):
    comp=get_object_or_404(componente,idcomp=id)
    datos={

        "componente":comp
    }

    return render(request,'aplicacion/detallecomponente.html', datos)


# Create your views here.