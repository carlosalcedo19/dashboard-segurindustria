from django.db import models
from apps.base.models import BaseModel


class Channel(BaseModel):
    name = models.CharField(verbose_name="Canal", max_length=255)
    description = models.CharField(verbose_name="Detalle de Canal", max_length=500)
    
    class Meta:
        verbose_name='Canal'
        verbose_name_plural= 'Canales'
        ordering = ('created_at',)
    
    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(verbose_name="Producto", max_length=255)
    detail = models.CharField(verbose_name="Detalles complementarios", max_length=500)

    class Meta:
        verbose_name='Producto'
        verbose_name_plural= 'Productos'
        ordering = ('created_at',)

    def __str__(self):
        return self.name
