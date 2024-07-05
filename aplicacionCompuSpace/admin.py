from django.contrib import admin
from .models import User,componente,pedido

# Register your models here.

admin.site.register(User)
admin.site.register(componente)
admin.site.register(pedido)