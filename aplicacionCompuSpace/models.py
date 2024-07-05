from django.db import models
from .listas import REGIONES, COMUNAS,MARCAS, ESTADOS
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone
import datetime


# Create your models here.

class User(AbstractUser):
    rut = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    region = models.CharField(max_length=50, choices=REGIONES)
    comuna = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)

class componente(models.Model):
    nombre = models.CharField(max_length=50)
    marca = models.CharField(max_length=50, choices=MARCAS)
    precio = models.IntegerField(validators=[MinValueValidator(0)])
    stock = models.IntegerField(validators=[MinValueValidator(0)])

class elementoCarrito(models.Model):
    componente = models.ForeignKey(componente,on_delete=models.CASCADE)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1,validators=[MinValueValidator(0)])

class pedido(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    estado = models.CharField(max_length=50, choices=ESTADOS, default="Preparando")
    fecha = models.DateTimeField(default=timezone.now)
    totalprecio = models.IntegerField()

class elementoPedido(models.Model):
    componente = models.ForeignKey(componente,on_delete=models.CASCADE)
    pedido = models.ForeignKey(pedido,on_delete=models.CASCADE)
    precio = models.IntegerField()
    cantidad = models.IntegerField(default=1,validators=[MinValueValidator(0)])