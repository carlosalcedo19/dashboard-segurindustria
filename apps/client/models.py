from django.db import models
from apps.base.models import BaseModel
from apps.client.choices import DocumentTypeChoices, SexoChoices

class Client(BaseModel):
    document_type = models.CharField(verbose_name="Tipo de documento", default=None, null=True, blank=True, max_length=30, choices=DocumentTypeChoices.choices)
    document_number = models.CharField('Código', max_length=10, null=True, blank=True,)
    full_name = models.CharField('Nombre completo', max_length=200, null=True, blank=True,)
    gender = models.CharField(verbose_name="Sexo", null=True, blank=True, default=None, max_length=30, choices=SexoChoices.choices)
    email= models.EmailField('Email', max_length=50, blank=True, null=True)
    phone = models.CharField(verbose_name='Télefono', blank=True)

    class Meta:
        verbose_name='Cliente'
        verbose_name_plural= 'Clientes'
        ordering = ('created_at',)
        
    def __str__(self):
        return f'{self.document_number} - {self.full_name}'
