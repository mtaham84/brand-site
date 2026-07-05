from django.core.cache import cache

def header_brands(request):
    brands = cache.get('menu_brands')
    if not brands:
        brands = Brand.objects.prefetch_related('categories').all()
        cache.set('menu_brands', brands, 60 * 10)
    return {'menu_brands': brands}