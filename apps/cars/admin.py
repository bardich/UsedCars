from django.contrib import admin
from .models import Category, Brand, Feature, Car, CarImage
from .forms import CarForm, CategoryForm, BrandForm, FeatureForm


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    fields = ['image', 'alt_text', 'is_featured', 'order']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    list_display = ['name', 'slug', 'is_active', 'order', 'created_at', 'car_count']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'order']
    
    def car_count(self, obj):
        return obj.cars.filter(published=True).count()
    car_count.short_description = 'Voitures'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    form = BrandForm
    list_display = ['name', 'slug', 'logo', 'car_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    def car_count(self, obj):
        return obj.cars.filter(published=True).count()
    car_count.short_description = 'Voitures'


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    form = FeatureForm
    list_display = ['name', 'icon']
    search_fields = ['name']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    form = CarForm
    list_display = ['title', 'brand', 'model_name', 'year', 'price', 'status', 'featured', 'published', 'created_at']
    list_filter = ['status', 'featured', 'published', 'brand', 'category', 'fuel_type', 'transmission', 'year']
    search_fields = ['title', 'brand__name', 'model_name', 'vin_number']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'featured', 'published', 'price']
    date_hierarchy = 'created_at'
    inlines = [CarImageInline]
    filter_horizontal = ['features']
    autocomplete_fields = ['brand', 'category']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('title', 'slug', 'category', 'brand', 'model_name')
        }),
        ('Spécifications techniques', {
            'fields': ('year', 'mileage', 'fuel_type', 'transmission', 'horsepower', 
                      'engine_size', 'drivetrain', 'color', 'doors', 'seats', 'condition')
        }),
        ('Immatriculation', {
            'fields': ('vin_number', 'registration_city'),
            'classes': ('collapse',)
        }),
        ('Description et prix', {
            'fields': ('description', 'price', 'negotiable_price')
        }),
        ('Statut et visibilité', {
            'fields': ('featured', 'status', 'published')
        }),
        ('Options', {
            'fields': ('features',),
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('brand', 'category')


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ['car', 'is_featured', 'order', 'created_at']
    list_filter = ['is_featured']
    list_editable = ['is_featured', 'order']
    autocomplete_fields = ['car']
