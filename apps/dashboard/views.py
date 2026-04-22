from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.contrib import messages
from apps.cars.models import Car, Category, Brand
from apps.cars.forms import CarForm, CategoryForm, BrandForm
from apps.core.models import SiteSettings
from apps.core.forms import SiteSettingsForm


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to ensure user is staff/admin"""
    def test_func(self):
        return self.request.user.is_staff


class DashboardView(AdminRequiredMixin, TemplateView):
    """Main dashboard view with stats"""
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tableau de bord'
        
        # Statistics
        context['total_cars'] = Car.objects.count()
        context['available_cars'] = Car.objects.filter(status=Car.STATUS_AVAILABLE).count()
        context['sold_cars'] = Car.objects.filter(status=Car.STATUS_SOLD).count()
        context['reserved_cars'] = Car.objects.filter(status=Car.STATUS_RESERVED).count()
        context['featured_cars'] = Car.objects.filter(featured=True).count()
        context['total_brands'] = Brand.objects.count()
        context['total_categories'] = Category.objects.count()
        
        return context


class CarManagementView(AdminRequiredMixin, ListView):
    """Car management list"""
    model = Car
    template_name = 'dashboard/cars.html'
    context_object_name = 'cars'
    paginate_by = 20

    def get_queryset(self):
        queryset = Car.objects.all().select_related('brand', 'category')
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(brand__name__icontains=search) |
                Q(model_name__icontains=search)
            )
        
        # Status filter
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Gestion des voitures'
        return context


class CarAddView(AdminRequiredMixin, CreateView):
    """Add new car view"""
    model = Car
    template_name = 'dashboard/car_form.html'
    form_class = CarForm
    success_url = reverse_lazy('dashboard:cars')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ajouter une voiture'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'La voiture "{form.instance}" a été créée avec succès.')
        return super().form_valid(form)


class CarEditView(AdminRequiredMixin, UpdateView):
    """Edit car view"""
    model = Car
    template_name = 'dashboard/car_form.html'
    form_class = CarForm
    success_url = reverse_lazy('dashboard:cars')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Modifier: {self.object}'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'La voiture "{form.instance}" a été mise à jour avec succès.')
        return super().form_valid(form)


class CarDeleteView(AdminRequiredMixin, DeleteView):
    """Delete car view"""
    model = Car
    template_name = 'dashboard/car_confirm_delete.html'
    success_url = reverse_lazy('dashboard:cars')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Supprimer: {self.object}'
        return context

    def delete(self, request, *args, **kwargs):
        car = self.get_object()
        messages.success(request, f'La voiture "{car}" a été supprimée.')
        return super().delete(request, *args, **kwargs)


# Category CRUD Views
class CategoryManagementView(AdminRequiredMixin, ListView):
    """Category management"""
    model = Category
    template_name = 'dashboard/categories.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Gestion des catégories'
        return context


class CategoryAddView(AdminRequiredMixin, CreateView):
    """Add new category"""
    model = Category
    template_name = 'dashboard/category_form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('dashboard:categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ajouter une catégorie'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'La catégorie "{form.instance.name}" a été créée.')
        return super().form_valid(form)


class CategoryEditView(AdminRequiredMixin, UpdateView):
    """Edit category"""
    model = Category
    template_name = 'dashboard/category_form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('dashboard:categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Modifier: {self.object}'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'La catégorie "{form.instance.name}" a été mise à jour.')
        return super().form_valid(form)


class CategoryDeleteView(AdminRequiredMixin, DeleteView):
    """Delete category"""
    model = Category
    template_name = 'dashboard/category_confirm_delete.html'
    success_url = reverse_lazy('dashboard:categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Supprimer: {self.object}'
        return context

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        messages.success(request, f'La catégorie "{category.name}" a été supprimée.')
        return super().delete(request, *args, **kwargs)


# Brand CRUD Views
class BrandManagementView(AdminRequiredMixin, ListView):
    """Brand management"""
    model = Brand
    template_name = 'dashboard/brands.html'
    context_object_name = 'brands'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Gestion des marques'
        return context


class BrandAddView(AdminRequiredMixin, CreateView):
    """Add new brand"""
    model = Brand
    template_name = 'dashboard/brand_form.html'
    form_class = BrandForm
    success_url = reverse_lazy('dashboard:brands')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ajouter une marque'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'La marque "{form.instance.name}" a été créée.')
        return super().form_valid(form)


class BrandEditView(AdminRequiredMixin, UpdateView):
    """Edit brand"""
    model = Brand
    template_name = 'dashboard/brand_form.html'
    form_class = BrandForm
    success_url = reverse_lazy('dashboard:brands')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Modifier: {self.object}'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'La marque "{form.instance.name}" a été mise à jour.')
        return super().form_valid(form)


class BrandDeleteView(AdminRequiredMixin, DeleteView):
    """Delete brand"""
    model = Brand
    template_name = 'dashboard/brand_confirm_delete.html'
    success_url = reverse_lazy('dashboard:brands')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Supprimer: {self.object}'
        return context

    def delete(self, request, *args, **kwargs):
        brand = self.get_object()
        messages.success(request, f'La marque "{brand.name}" a été supprimée.')
        return super().delete(request, *args, **kwargs)


class SiteSettingsUpdateView(AdminRequiredMixin, UpdateView):
    """Update site settings"""
    model = SiteSettings
    form_class = SiteSettingsForm
    template_name = 'dashboard/site_settings.html'
    success_url = reverse_lazy('dashboard:site_settings')

    def get_object(self, queryset=None):
        """Get or create the singleton settings instance"""
        return SiteSettings.get_settings()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Paramètres du site'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Les paramètres du site ont été mis à jour avec succès.')
        return super().form_valid(form)
