from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from apps.core.models import TimeStampedModel
from .managers import CarManager, BrandManager, CategoryManager


class Category(TimeStampedModel):
    """Car category model"""
    name = models.CharField(max_length=100, verbose_name='Nom')
    slug = models.SlugField(unique=True)
    icon = models.ImageField(upload_to='categories/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    # Custom manager
    objects = CategoryManager()

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('cars:list') + f'?category={self.slug}'


class Brand(TimeStampedModel):
    """Car brand model"""
    name = models.CharField(max_length=100, verbose_name='Marque')
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    
    # Custom manager
    objects = BrandManager()

    class Meta:
        verbose_name = 'Marque'
        verbose_name_plural = 'Marques'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('cars:list') + f'?brand={self.slug}'


class Feature(TimeStampedModel):
    """Car feature/options model"""
    name = models.CharField(max_length=100, verbose_name='Option')
    icon = models.CharField(max_length=50, blank=True, help_text='Icon class (e.g., fas fa-snowflake)')

    class Meta:
        verbose_name = 'Option'
        verbose_name_plural = 'Options'
        ordering = ['name']

    def __str__(self):
        return self.name


class Car(TimeStampedModel):
    """Car listing model"""
    
    # Status choices
    STATUS_AVAILABLE = 'available'
    STATUS_RESERVED = 'reserved'
    STATUS_SOLD = 'sold'
    
    STATUS_CHOICES = [
        (STATUS_AVAILABLE, 'Disponible'),
        (STATUS_RESERVED, 'Réservée'),
        (STATUS_SOLD, 'Vendue'),
    ]
    
    # Fuel type choices
    FUEL_PETROL = 'petrol'
    FUEL_DIESEL = 'diesel'
    FUEL_HYBRID = 'hybrid'
    FUEL_ELECTRIC = 'electric'
    
    FUEL_CHOICES = [
        (FUEL_PETROL, 'Essence'),
        (FUEL_DIESEL, 'Diesel'),
        (FUEL_HYBRID, 'Hybride'),
        (FUEL_ELECTRIC, 'Électrique'),
    ]
    
    # Transmission choices
    TRANS_MANUAL = 'manual'
    TRANS_AUTOMATIC = 'automatic'
    TRANS_SEMI_AUTO = 'semi_auto'
    
    TRANS_CHOICES = [
        (TRANS_MANUAL, 'Manuelle'),
        (TRANS_AUTOMATIC, 'Automatique'),
        (TRANS_SEMI_AUTO, 'Semi-automatique'),
    ]
    
    # Drivetrain choices
    DRIVE_FWD = 'fwd'
    DRIVE_RWD = 'rwd'
    DRIVE_AWD = 'awd'
    DRIVE_4WD = '4wd'
    
    DRIVE_CHOICES = [
        (DRIVE_FWD, 'Traction avant'),
        (DRIVE_RWD, 'Propulsion'),
        (DRIVE_AWD, 'Intégrale'),
        (DRIVE_4WD, '4x4'),
    ]
    
    # Condition choices
    CONDITION_NEW = 'new'
    CONDITION_EXCELLENT = 'excellent'
    CONDITION_GOOD = 'good'
    CONDITION_FAIR = 'fair'
    
    CONDITION_CHOICES = [
        (CONDITION_NEW, 'Neuf'),
        (CONDITION_EXCELLENT, 'Excellent'),
        (CONDITION_GOOD, 'Bon état'),
        (CONDITION_FAIR, 'État correct'),
    ]
    
    # Basic info
    title = models.CharField(max_length=200, verbose_name='Titre')
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='cars', verbose_name='Catégorie')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name='cars', verbose_name='Marque')
    model_name = models.CharField(max_length=100, verbose_name='Modèle')
    
    # Specifications
    year = models.PositiveIntegerField(verbose_name='Année')
    mileage = models.PositiveIntegerField(verbose_name='Kilométrage')
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default=FUEL_PETROL, verbose_name='Carburant')
    transmission = models.CharField(max_length=20, choices=TRANS_CHOICES, default=TRANS_MANUAL, verbose_name='Transmission')
    horsepower = models.PositiveIntegerField(blank=True, null=True, verbose_name='Puissance (ch)')
    engine_size = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, verbose_name='Cylindrée (L)')
    drivetrain = models.CharField(max_length=10, choices=DRIVE_CHOICES, default=DRIVE_FWD, verbose_name='Transmission')
    color = models.CharField(max_length=50, blank=True, verbose_name='Couleur')
    doors = models.PositiveIntegerField(default=4, verbose_name='Portes')
    seats = models.PositiveIntegerField(default=5, verbose_name='Places')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default=CONDITION_EXCELLENT, verbose_name='État')
    
    # Registration
    vin_number = models.CharField(max_length=17, blank=True, verbose_name='N° de série')
    registration_city = models.CharField(max_length=50, blank=True, verbose_name='Ville d\'immatriculation')
    
    # Description
    description = models.TextField(blank=True, verbose_name='Description')
    
    # Pricing
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='Prix (MAD)')
    negotiable_price = models.BooleanField(default=False, verbose_name='Prix négociable')
    
    # Status & Visibility
    featured = models.BooleanField(default=False, verbose_name='En vedette')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE, verbose_name='Statut')
    published = models.BooleanField(default=True, verbose_name='Publiée')
    
    # Features
    features = models.ManyToManyField(Feature, blank=True, related_name='cars', verbose_name='Options')
    
    # Custom manager
    objects = CarManager()
    
    class Meta:
        verbose_name = 'Voiture'
        verbose_name_plural = 'Voitures'
        ordering = ['-featured', '-created_at']
    
    def __str__(self):
        return f"{self.brand.name} {self.model_name} {self.year}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.brand.name}-{self.model_name}-{self.year}-{self.id}")
        if not self.title:
            self.title = f"{self.brand.name} {self.model_name} {self.year}"
        super().save(*args, **kwargs)
        # Update slug after save if it includes id
        if not self.slug or str(self.id) not in self.slug:
            self.slug = slugify(f"{self.brand.name}-{self.model_name}-{self.year}-{self.id}")
            Car.objects.filter(id=self.id).update(slug=self.slug)
    
    def get_absolute_url(self):
        return reverse('cars:detail', kwargs={'slug': self.slug})
    
    def get_main_image(self):
        """Returns the featured image or first image"""
        featured = self.images.filter(is_featured=True).first()
        if featured:
            return featured
        return self.images.first()
    
    @property
    def is_available(self):
        return self.status == self.STATUS_AVAILABLE
    
    @property
    def is_reserved(self):
        return self.status == self.STATUS_RESERVED
    
    @property
    def is_sold(self):
        return self.status == self.STATUS_SOLD


class CarImage(TimeStampedModel):
    """Car images model"""
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cars/%Y/%m/', verbose_name='Image')
    alt_text = models.CharField(max_length=200, blank=True, verbose_name='Texte alternatif')
    is_featured = models.BooleanField(default=False, verbose_name='Image principale')
    order = models.PositiveIntegerField(default=0, verbose_name='Ordre')
    
    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        ordering = ['order', '-is_featured', 'created_at']
    
    def __str__(self):
        return f"Image de {self.car}"
    
    def save(self, *args, **kwargs):
        # Ensure only one featured image per car
        if self.is_featured:
            CarImage.objects.filter(car=self.car, is_featured=True).update(is_featured=False)
        super().save(*args, **kwargs)
