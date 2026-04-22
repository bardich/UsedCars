from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.AnalyticsView.as_view(), name='index'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
    path('inquiries/', views.InquiryListView.as_view(), name='inquiries'),
    path('inquiries/<int:pk>/', views.InquiryUpdateView.as_view(), name='inquiry_update'),
]
