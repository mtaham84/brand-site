from django.contrib import admin
from .models import Brand, Category, Product, HomeBanner
from .models import PromoGif
from .models import BeforeAfter

class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'name_fa', 'order']
    inlines = [CategoryInline]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'brand', 'category', 'rate', 'is_best_seller']
    list_filter = ['brand', 'category', 'is_best_seller']

@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'position', 'active', 'order']
    list_filter = ['position', 'active']

@admin.register(PromoGif)
class PromoGifAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']

@admin.register(BeforeAfter)
class BeforeAfterAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']

from .models import CatalogPDF, ContactRequest

@admin.register(CatalogPDF)
class CatalogPDFAdmin(admin.ModelAdmin):
    list_display = ['title', 'language', 'download_count', 'pdf_file'] 
    list_filter = ['language']
    readonly_fields = ['download_count']


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'created_at']
    search_fields = ['name', 'phone', 'email']
    readonly_fields = ['created_at']