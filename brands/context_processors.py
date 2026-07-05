from .models import Brand

def header_brands(request):
    return {
        'menu_brands': Brand.objects.only(
            'id',
            'name_en',
            'name_fa'
        )
    }

def language_processor(request):
    return {'LANG': request.LANGUAGE_CODE[:2]}