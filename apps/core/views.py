from django.shortcuts import render
from django.views.generic import TemplateView
from apps.cars.models import Car, Category, Brand


def error_404(request, exception=None):
    """Custom 404 error handler"""
    return render(request, 'errors/404.html', status=404)


def error_500(request, exception=None):
    """Custom 500 error handler"""
    return render(request, 'errors/500.html', status=500)


class HomePageView(TemplateView):
    """Homepage view"""
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Accueil'
        
        # Featured cars
        context['featured_cars'] = Car.objects.filter(
            featured=True,
            published=True,
            status=Car.STATUS_AVAILABLE
        ).select_related('brand', 'category').prefetch_related('images')[:6]
        
        # Latest cars
        context['latest_cars'] = Car.objects.filter(
            published=True
        ).select_related('brand').prefetch_related('images')[:4]
        
        # Brands for filter
        context['brands'] = Brand.objects.filter(
            cars__published=True
        ).distinct()
        
        # Categories
        context['categories'] = Category.objects.filter(
            is_active=True,
            cars__published=True
        ).distinct()
        
        # Years for filter dropdown (current year down to 2010)
        from datetime import datetime
        current_year = datetime.now().year
        context['years'] = list(range(current_year, 2009, -1))
        
        return context
