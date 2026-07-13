from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('brand/<int:brand_id>/', views.brand_detail, name='brand_detail'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('best-sellers/', views.best_sellers, name='best_sellers'),
    path('contact/', views.contact, name='contact'),
    path('catalogs/', views.catalog_with_contact, name='catalog_with_contact'),
    path('catalog/download/<int:pdf_id>/', views.catalog_download, name='catalog_download'),
    path('about/', views.about, name='about'),
    
    
]