from django.db import models
from apps.base.models import BaseModel
from apps.client.choices import DocumentTypeChoices, PersonTypeChoices

class Company(BaseModel):
    name = models.CharField(verbose_name="Empresa",max_length=255 )
    ruc = models.CharField( verbose_name="RUC", max_length=11, null=True,blank=True, unique=True)
    industry = models.CharField(verbose_name="Rubro",max_length=255,null=True,blank=True )
    

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.name


class Client(BaseModel):
    person_type = models.CharField( verbose_name="Tipo de Cliente", max_length=20,choices= PersonTypeChoices.choices, default="natural")
    company = models.ForeignKey(Company, verbose_name="Empresa", on_delete=models.SET_NULL, null=True,blank=True,related_name="company_clients" )
    document_type = models.CharField(verbose_name="Tipo de documento", default=None, null=True, blank=True, max_length=30, choices=DocumentTypeChoices.choices)
    document_number = models.CharField('Código', max_length=10, null=True, blank=True, unique=True)
    first_name = models.CharField('Nombres', max_length=200, null=True, blank=True,)
    last_name = models.CharField('Apellidos', max_length=200, null=True, blank=True,)
    position = models.CharField(verbose_name="Cargo",max_length=255,null=True,blank=True)
    email= models.EmailField('Email', max_length=50, blank=True, null=True)
    phone = models.CharField(verbose_name='Télefono', blank=True)
   


    class Meta:
        verbose_name='Cliente'
        verbose_name_plural= 'Clientes'
        ordering = ('created_at',)
        
    def __str__(self):
        return f'{self.document_number} - {self.first_name} -{self.last_name}'
