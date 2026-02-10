from django.db.models import TextChoices

class LeadStatusChoices(TextChoices):
    NV = 'Nuevo', 'Nuevo'
    EC = 'En contacto', 'En contacto'
    CO = 'Cotizado', 'Cotizado'
    VE = 'Vendido', 'Vendido'
    PE = 'Perdido', 'Perdido'

class ReasonChoices(TextChoices):
    CO = "Competencia", "Competencia"
    FS = "Falta de Stock", "Falta de Stock"
    DFT = "Despacho fuera de tiempo","Despacho fuera de tiempo"
    PP = "Precio de Producto", "Precio de Producto"