from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel
from apps.cars.models import Car

User = get_user_model()


class CarView(TimeStampedModel):
    """Track car views for analytics"""
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='view_records')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Vue'
        verbose_name_plural = 'Vues'


class Inquiry(TimeStampedModel):
    """Track customer inquiries"""
    STATUS_CHOICES = [
        ('new', 'Nouveau'),
        ('contacted', 'Contacté'),
        ('closed', 'Clôturé'),
    ]
    SOURCE_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('phone', 'Téléphone'),
        ('email', 'Email'),
        ('form', 'Formulaire'),
    ]
    
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True, related_name='inquiries')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    message = models.TextField(blank=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='form')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Demande'
        verbose_name_plural = 'Demandes'
        ordering = ['-created_at']

    def __str__(self):
        return f"Demande de {self.name}"
