from django.views.generic import TemplateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Sum, Q, Avg
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from apps.cars.models import Car, Brand
from apps.analytics.models import CarView, Inquiry


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class AnalyticsView(AdminRequiredMixin, TemplateView):
    """Analytics dashboard view with chart data"""
    template_name = 'analytics/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Analytiques'
        
        # Inventory stats
        context['inventory_stats'] = self.get_inventory_stats()
        
        # Monthly stats
        context['monthly_data'] = self.get_monthly_stats()
        
        # Popular cars (last 30 days)
        context['popular_cars'] = self.get_popular_cars()
        
        # Popular brands
        context['popular_brands'] = self.get_popular_brands()
        
        # Inquiry stats
        context['inquiry_stats'] = self.get_inquiry_stats()
        
        return context
    
    def get_inventory_stats(self):
        """Get inventory by status"""
        stats = {
            'labels': ['Disponible', 'Réservé', 'Vendu'],
            'data': [
                Car.objects.filter(status=Car.STATUS_AVAILABLE).count(),
                Car.objects.filter(status=Car.STATUS_RESERVED).count(),
                Car.objects.filter(status=Car.STATUS_SOLD).count(),
            ],
            'colors': ['#22c55e', '#eab308', '#6b7280']
        }
        return stats
    
    def get_monthly_stats(self):
        """Get cars added and sold by month (last 6 months)"""
        months = []
        added_data = []
        sold_data = []
        
        for i in range(5, -1, -1):
            date = timezone.now() - timedelta(days=i * 30)
            month_label = date.strftime('%b %Y')
            month_start = date.replace(day=1)
            
            months.append(month_label)
            
            # Cars added
            added_count = Car.objects.filter(
                created_at__year=date.year,
                created_at__month=date.month
            ).count()
            added_data.append(added_count)
            
            # Cars sold
            sold_count = Car.objects.filter(
                status=Car.STATUS_SOLD,
                updated_at__year=date.year,
                updated_at__month=date.month
            ).count()
            sold_data.append(sold_count)
        
        return {
            'labels': months,
            'added': added_data,
            'sold': sold_data
        }
    
    def get_popular_cars(self):
        """Get most viewed cars"""
        return Car.objects.filter(published=True).annotate(
            view_count=Count('view_records')
        ).order_by('-view_count')[:5]
    
    def get_popular_brands(self):
        """Get brands with most cars"""
        return Brand.objects.annotate(
            car_count=Count('cars', filter=Q(cars__published=True))
        ).filter(car_count__gt=0).order_by('-car_count')[:5]
    
    def get_inquiry_stats(self):
        """Get inquiry statistics"""
        return {
            'total': Inquiry.objects.count(),
            'new': Inquiry.objects.filter(status='new').count(),
            'contacted': Inquiry.objects.filter(status='contacted').count(),
            'closed': Inquiry.objects.filter(status='closed').count(),
        }


class InquiryListView(AdminRequiredMixin, ListView):
    """Inquiry management list"""
    model = Inquiry
    template_name = 'analytics/inquiries.html'
    context_object_name = 'inquiries'
    paginate_by = 20
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Demandes clients'
        return context


class InquiryUpdateView(AdminRequiredMixin, UpdateView):
    """Update inquiry status"""
    model = Inquiry
    template_name = 'analytics/inquiry_form.html'
    fields = ['status', 'notes']
    success_url = '/analytics/inquiries/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Demande de {self.object.name}'
        return context


class ReportsView(AdminRequiredMixin, TemplateView):
    """Reports view"""
    template_name = 'analytics/reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Rapports'
        
        # Revenue estimate from sold cars
        revenue_data = Car.objects.filter(
            status=Car.STATUS_SOLD
        ).aggregate(
            total_revenue=Sum('price'),
            avg_price=Avg('price'),
            count=Count('id')
        )
        
        context['revenue'] = revenue_data['total_revenue'] or 0
        context['avg_price'] = revenue_data['avg_price'] or 0
        context['sold_count'] = revenue_data['count']
        
        # Price range distribution
        context['price_distribution'] = self.get_price_distribution()
        
        return context
    
    def get_price_distribution(self):
        """Get price range distribution"""
        ranges = [
            ('0 - 50,000 MAD', 0, 50000),
            ('50,000 - 100,000 MAD', 50000, 100000),
            ('100,000 - 200,000 MAD', 100000, 200000),
            ('200,000 - 500,000 MAD', 200000, 500000),
            ('500,000+ MAD', 500000, 999999999),
        ]
        
        labels = []
        data = []
        
        for label, min_price, max_price in ranges:
            labels.append(label)
            count = Car.objects.filter(
                price__gte=min_price,
                price__lt=max_price,
                published=True
            ).count()
            data.append(count)
        
        return {'labels': labels, 'data': data}
