from django.shortcuts import render, get_object_or_404
from .models import BeforeAfter, Brand, Category, Product, HomeBanner, PromoGif
from django.shortcuts import render
from .models import CatalogPDF, ContactRequest
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django import forms
import re

def home(request):
    top_banners = HomeBanner.objects.filter(active=True, position='top')
    bottom_banners = HomeBanner.objects.filter(active=True, position='bottom')
    # پرفروش‌ترین‌ها
    best_sellers = Product.objects.filter(is_best_seller=True)[:8]
    # محصولات هر برند برای نوارها (نمونه ۶ محصول اول)
    brands = Brand.objects.prefetch_related('products').all()
    brand_products = {}
    for brand in brands:
        brand_products[brand] = brand.products.all()[:6]
    promo_gifs = PromoGif.objects.filter(active=True)
    before_after_list = BeforeAfter.objects.filter(active=True)
    context = {

        'top_banners': top_banners,
        'bottom_banners': bottom_banners,
        'best_sellers': best_sellers,
        'brand_products': brand_products,
        'promo_gifs': promo_gifs,
        'before_after_list': before_after_list,
    }
    return render(request, 'brands/home.html', context)

def brand_detail(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    products = brand.products.all()
    context = {'brand': brand, 'products': products}
    return render(request, 'brands/brand_detail.html', context)

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.products.all()
    context = {'category': category, 'products': products}
    return render(request, 'brands/category_detail.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product_id)[:4]
    context = {'product': product, 'related_products': related_products}
    return render(request, 'brands/product_detail.html', context)

def best_sellers(request):
    products = Product.objects.filter(is_best_seller=True)
    context = {'products': products}
    return render(request, 'brands/best_sellers.html', context)

def contact(request):
    context = {
        'phone': '+98 21 4404 5581',
        'address_fa': 'ایران، تهران، فلکه دوم صادقیه، کوچه شهید دهزویی',
        'address_en': 'No. 5, Shahid Dehzouei Alley, 2nd Sadeghiyeh Square, Tehran, Iran',
        'email': 'zibasazzcom@gmail.com',
    }
    return render(request, 'brands/contact.html', context)




class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'phone', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
     cleaned_data = super().clean()
     phone = cleaned_data.get('phone')
     email = cleaned_data.get('email')

     if not phone and not email:
        raise forms.ValidationError("حداقل یکی از شماره تماس یا ایمیل باید پر شود.")

     if phone:
        # شماره می‌تواند شامل +، -، فاصله، پرانتز و حداقل ۷ رقم باشد
        import re
        pattern = r'^[\d\s()+-]{7,25}$'
        if not re.match(pattern, phone.strip()):
            raise forms.ValidationError(
                "شماره تماس نامعتبر است. لطفاً یک شماره تلفن معتبر (ثابت یا همراه) وارد کنید."
            )
        # حذف نویسه‌های اضافی برای بررسی تعداد ارقام واقعی
        digits_only = re.sub(r'\D', '', phone)
        if len(digits_only) < 7:
            raise forms.ValidationError(
                "شماره تماس باید حداقل ۷ رقم داشته باشد."
            )

     if email:
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("ایمیل نامعتبر است.")

     return cleaned_data


def catalog_with_contact(request):
    lang = request.LANGUAGE_CODE[:2]  # 'en' or 'fa'
    pdfs = CatalogPDF.objects.filter(language=lang)
    success = False
    form = ContactRequestForm()

    if request.method == 'POST':
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = ContactRequestForm()  # پاک‌کردن فرم بعد از ثبت

    context = {
        'pdfs': pdfs,
        'form': form,
        'success': success,
    }
    return render(request, 'brands/catalog_with_contact.html', context)

from django.http import FileResponse, Http404

def catalog_download(request, pdf_id):
    pdf = get_object_or_404(CatalogPDF, id=pdf_id)
    # افزایش شمارنده دانلود
    pdf.download_count += 1
    pdf.save(update_fields=['download_count'])
    
    try:
        return FileResponse(pdf.pdf_file, as_attachment=True)
    except FileNotFoundError:
        raise Http404("File not found")
    
from django.shortcuts import render

def about(request):
    return render(request, 'about.html')