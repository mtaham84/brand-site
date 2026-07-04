from .models import Brand

def header_brands(request):
    brands = Brand.objects.prefetch_related('categories').all()
    return {'menu_brands': brands}

def language_processor(request):
    # زبان جاری را به قالب ارسال می‌کنیم (en یا fa)
    return {'LANG': request.LANGUAGE_CODE[:2]}  # 'en' یا 'fa'