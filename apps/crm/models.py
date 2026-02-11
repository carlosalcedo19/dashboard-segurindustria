from django.db import models
from apps.base.models import BaseModel
from django.conf import settings
from apps.crm.choices import LeadStatusChoices, ReasonChoices
from apps.users.models import User
from apps.maintenance.models import Channel, Product
from apps.client.models import Client
from apps.maintenance.models import Fair, ProductLine

class Lead(BaseModel):
    client = models.ForeignKey(Client, verbose_name="Cliente", on_delete=models.CASCADE,null=True, blank=True, related_name="client_lead")
    channel = models.ForeignKey(Channel,verbose_name="Canal", on_delete=models.CASCADE,null=True, blank=True, related_name="channel_lead")
    fair = models.ForeignKey(Fair, verbose_name="Feria",on_delete=models.SET_NULL, null=True, blank=True, related_name="fair_lead")
    agent = models.ForeignKey(User, verbose_name="Asesor", on_delete=models.CASCADE,null=True, blank=True, related_name="agent_lead")
    product_line = models.ForeignKey(ProductLine, verbose_name="Línea de Producto de Interés", on_delete=models.SET_NULL, null=True, blank=True, related_name="productline_lead")
    product = models.ForeignKey(Product, verbose_name="Producto", on_delete=models.CASCADE,null=True, blank=True, related_name="product_lead")
    status = models.CharField(verbose_name="Estado", max_length=50,choices= LeadStatusChoices.choices)
    amount = models.DecimalField(verbose_name="Monto", max_digits=12,decimal_places=2, default=0, null=True, blank=True,)
    reason = models.CharField(verbose_name="Razón", max_length=100, blank=True, null=True, choices= ReasonChoices.choices, )
    date =  models.DateField(verbose_name='Fecha de contacto', help_text='Fecha de inicio de contacto')

    class Meta:
        verbose_name='Lead'
        verbose_name_plural= 'Leads'
        ordering = ('created_at',)
    

    def __str__(self):
        return f"{self.client.first_name} - {self.client.last_name}" if self.client else f"Lead #{self.id}"
