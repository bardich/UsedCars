from django.db import models
from django.db.models import Q


class CarQuerySet(models.QuerySet):
    """Custom QuerySet for Car model"""
    
    def available(self):
        """Return only available cars"""
        return self.filter(status='available', published=True)
    
    def featured(self):
        """Return featured cars"""
        return self.filter(featured=True, published=True)
    
    def published(self):
        """Return all published cars"""
        return self.filter(published=True)
    
    def by_brand(self, brand_slug):
        """Filter by brand slug"""
        return self.filter(brand__slug=brand_slug, published=True)
    
    def by_category(self, category_slug):
        """Filter by category slug"""
        return self.filter(category__slug=category_slug, published=True)
    
    def by_price_range(self, min_price=None, max_price=None):
        """Filter by price range"""
        qs = self
        if min_price is not None:
            qs = qs.filter(price__gte=min_price)
        if max_price is not None:
            qs = qs.filter(price__lte=max_price)
        return qs
    
    def by_year_range(self, min_year=None, max_year=None):
        """Filter by year range"""
        qs = self
        if min_year is not None:
            qs = qs.filter(year__gte=min_year)
        if max_year is not None:
            qs = qs.filter(year__lte=max_year)
        return qs
    
    def search(self, query):
        """Search cars by query string"""
        if not query:
            return self
        return self.filter(
            Q(title__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(model_name__icontains=query) |
            Q(description__icontains=query)
        )
    
    def with_images(self):
        """Prefetch related images for optimization"""
        return self.prefetch_related('images')
    
    def with_all_relations(self):
        """Select and prefetch all related data for optimization"""
        return self.select_related('brand', 'category').prefetch_related('images', 'features')


class CarManager(models.Manager):
    """Custom Manager for Car model"""
    
    def get_queryset(self):
        return CarQuerySet(self.model, using=self._db)
    
    def available(self):
        return self.get_queryset().available()
    
    def featured(self):
        return self.get_queryset().featured()
    
    def published(self):
        return self.get_queryset().published()
    
    def by_brand(self, brand_slug):
        return self.get_queryset().by_brand(brand_slug)
    
    def by_category(self, category_slug):
        return self.get_queryset().by_category(category_slug)
    
    def by_price_range(self, min_price=None, max_price=None):
        return self.get_queryset().by_price_range(min_price, max_price)
    
    def search(self, query):
        return self.get_queryset().search(query)


class BrandQuerySet(models.QuerySet):
    """Custom QuerySet for Brand model"""
    
    def with_car_count(self):
        """Annotate with car count"""
        return self.annotate(car_count=models.Count('cars'))
    
    def active(self):
        """Brands that have published cars"""
        return self.filter(cars__published=True).distinct()


class BrandManager(models.Manager):
    """Custom Manager for Brand model"""
    
    def get_queryset(self):
        return BrandQuerySet(self.model, using=self._db)
    
    def with_car_count(self):
        return self.get_queryset().with_car_count()
    
    def active(self):
        return self.get_queryset().active()


class CategoryQuerySet(models.QuerySet):
    """Custom QuerySet for Category model"""
    
    def active(self):
        """Return only active categories"""
        return self.filter(is_active=True)
    
    def with_car_count(self):
        """Annotate with car count"""
        return self.annotate(car_count=models.Count('cars'))


class CategoryManager(models.Manager):
    """Custom Manager for Category model"""
    
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def with_car_count(self):
        return self.get_queryset().with_car_count()
