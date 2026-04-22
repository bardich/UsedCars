from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Car, Brand, Category


class CarListView(ListView):
    """Car listing view with filters"""
    model = Car
    template_name = 'cars/list.html'
    context_object_name = 'cars'
    paginate_by = 12

    def get_queryset(self):
        queryset = Car.objects.filter(published=True)
        
        # Search filter
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(brand__name__icontains=search) |
                Q(model_name__icontains=search)
            )
        
        # Brand filter
        brand = self.request.GET.get('brand')
        if brand:
            queryset = queryset.filter(brand__slug=brand)
        
        # Category filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Price range
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        
        # Year filter
        year_min = self.request.GET.get('year_min')
        if year_min:
            queryset = queryset.filter(year__gte=year_min)
        
        # Sorting
        sort = self.request.GET.get('sort', '-created_at')
        queryset = queryset.order_by(sort)
        
        return queryset.select_related('brand', 'category').prefetch_related('images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nos Voitures'
        
        # Filter options
        context['brands'] = Brand.objects.filter(
            cars__published=True
        ).distinct().order_by('name')
        
        context['categories'] = Category.objects.filter(
            is_active=True,
            cars__published=True
        ).distinct().order_by('name')
        
        return context


class CarDetailView(DetailView):
    """Car detail view"""
    model = Car
    template_name = 'cars/detail.html'
    context_object_name = 'car'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Car.objects.filter(published=True).select_related('brand', 'category').prefetch_related('images', 'features')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.object
        context['title'] = f"{car.brand.name} {car.model_name} {car.year}"
        
        # Similar cars
        context['similar_cars'] = Car.objects.filter(
            category=car.category,
            published=True
        ).exclude(id=car.id)[:4]
        
        return context
