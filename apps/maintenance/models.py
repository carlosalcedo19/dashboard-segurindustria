from django.db import models
from apps.base.models import BaseModel
from apps.maintenance.choices import ChannelTypeChoices


class Fair(BaseModel):
    name = models.CharField(verbose_name="Nombre de Feria", max_length=255)
    start_date= models.DateField(verbose_name="Fecha de Inicio", null=True, blank=True,)
    end_date= models.DateField(verbose_name="Fecha de Fin", null=True, blank=True,)
    place = models.CharField(verbose_name="Lugar de Feria", null=True, blank=True,)

    class Meta:
        verbose_name='Feria'
        verbose_name_plural= 'Ferias'
        ordering = ('created_at',)

    def __str__(self):
        return self.name

class Channel(BaseModel):
    name = models.CharField(verbose_name="Canal", max_length=255, null=True, blank=True,)
    channel_type= models.CharField(verbose_name="Tipo de Canal", max_length=255, null=True, choices= ChannelTypeChoices.choices)
    description = models.CharField(verbose_name="Detalle de Canal", max_length=500, null=True, blank=True,)
    
    class Meta:
        verbose_name='Canal'
        verbose_name_plural= 'Canales'
        ordering = ('created_at',)
    
    def __str__(self):
        return self.name

class ProductLine(BaseModel):
    name = models.CharField(verbose_name="Nombre de Linea",max_length=255)
    detail = models.CharField(verbose_name="Detalles complementarios", max_length=500, null=True, blank=True,)

    class Meta:
        verbose_name='Línea de Producto'
        verbose_name_plural= 'Líneas de Productos'
        ordering = ('created_at',)

    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(verbose_name="Producto", max_length=255)
    productline = models.ForeignKey(ProductLine, verbose_name="Línea de Producto", on_delete=models.CASCADE,null=True, blank=True, related_name="productline_product")
    detail = models.CharField(verbose_name="Detalles complementarios", max_length=500, null=True, blank=True,)

    class Meta:
        verbose_name='Producto'
        verbose_name_plural= 'Productos'
        ordering = ('created_at',)

    def __str__(self):
        return self.name
    

