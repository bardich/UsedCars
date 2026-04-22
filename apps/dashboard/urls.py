from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='index'),
    # Car management
    path('cars/', views.CarManagementView.as_view(), name='cars'),
    path('cars/add/', views.CarAddView.as_view(), name='car_add'),
    path('cars/<int:pk>/edit/', views.CarEditView.as_view(), name='car_edit'),
    path('cars/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car_delete'),
    # Category management
    path('categories/', views.CategoryManagementView.as_view(), name='categories'),
    path('categories/add/', views.CategoryAddView.as_view(), name='category_add'),
    path('categories/<int:pk>/edit/', views.CategoryEditView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    # Brand management
    path('brands/', views.BrandManagementView.as_view(), name='brands'),
    path('brands/add/', views.BrandAddView.as_view(), name='brand_add'),
    path('brands/<int:pk>/edit/', views.BrandEditView.as_view(), name='brand_edit'),
    path('brands/<int:pk>/delete/', views.BrandDeleteView.as_view(), name='brand_delete'),
    # Site settings
    path('settings/', views.SiteSettingsUpdateView.as_view(), name='site_settings'),
]
