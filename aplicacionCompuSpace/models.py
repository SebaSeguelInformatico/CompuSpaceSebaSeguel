from django.db import models
from .listas import REGIONES, COMUNAS,MARCAS
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser, User


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
