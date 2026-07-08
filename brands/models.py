from django.db import models
import fitz  # PyMuPDF
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from .utils import optimize_image
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from ckeditor.fields import RichTextField


class Brand(models.Model):
    name_en = models.CharField(max_length=100)
    name_fa = models.CharField(max_length=100)
    description_en = models.TextField(blank=True)
    description_fa = models.TextField(blank=True)
    logo = models.ImageField(upload_to='brands/logos/')
    banner = models.ImageField(upload_to='brands/banners/', blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name_en


class Category(models.Model):
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    name_en = models.CharField(max_length=100)
    name_fa = models.CharField(max_length=100)
    slug = models.SlugField(unique=False, blank=True)

    def __str__(self):
        return f"{self.brand.name_en} - {self.name_en}"


class Product(models.Model):
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='products'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name_en = models.CharField(max_length=200)
    name_fa = models.CharField(max_length=200)
    description_fa = RichTextField()
    description_en = RichTextField()
    image = models.ImageField(upload_to='products/')
    image_secondary = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="تصویر دوم")
    rate = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=4.0
    )  # مقیاس 0 تا 5
    is_best_seller = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
      if self.image:
        self.image = optimize_image(self.image)

      if self.image_secondary:
        self.image_secondary = optimize_image(self.image_secondary)

      super().save(*args, **kwargs)

    def __str__(self):
        return self.name_en


class HomeBanner(models.Model):
    POSITION_CHOICES = [
        ('top', 'بالای صفحه'),
        ('bottom', 'پایین صفحه'),
    ]
    title_en = models.CharField(max_length=200, blank=True)
    title_fa = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES, default='top')
    order = models.IntegerField(default=0)
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.get_position_display()} - {self.title_en or 'Banner'}"

    

class PromoGif(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='promo_images/', blank=True, null=True)   # برای گیف یا عکس ثابت
    video = models.FileField(upload_to='promo_videos/', blank=True, null=True)    # برای ویدیو (mp4, webm)
    link = models.URLField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title or "Promo Media"
    
class BeforeAfter(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image_before = models.ImageField(upload_to='before_after/')
    image_after  = models.ImageField(upload_to='before_after/')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title or "Before/After"
    
class CatalogPDF(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('fa', 'Persian'),
    ]
    title = models.CharField(max_length=100, blank=True)
    pdf_file = models.FileField(upload_to='catalogs/')
    cover_image = models.ImageField(upload_to='catalogs/covers/', blank=True, null=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    download_count = models.IntegerField(default=0) # ⭐️ فیلد اضافه شده برای رفع خطای ادمین

    def __str__(self):
        return f"{self.title or 'Catalog'} ({self.get_language_display()})"


@receiver(post_save, sender=CatalogPDF)
def generate_pdf_cover(sender, instance, created, **kwargs):
    if created and instance.pdf_file and not instance.cover_image:
        try:
            # باز کردن PDF با PyMuPDF
            pdf_document = fitz.open(instance.pdf_file.path)
            first_page = pdf_document.load_page(0)
            # تبدیل به تصویر با رزولوشن مناسب (ماتریس ۲ برابر بزرگ‌تر)
            pix = first_page.get_pixmap(matrix=fitz.Matrix(2, 2))
            
            # ذخیره در فیلد cover_image
            img_byte = pix.tobytes("png")
            img_name = f"{os.path.splitext(os.path.basename(instance.pdf_file.name))[0]}_cover.png"
            instance.cover_image.save(img_name, ContentFile(img_byte), save=True)
            pdf_document.close()
        except Exception as e:
            # در صورت خطا از ادامه جلوگیری نمی‌کنیم
            print(f"Error generating PDF cover: {e}")


class ContactRequest(models.Model):
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.name or self.phone or self.email}"

    class Meta:
        verbose_name = "Contact Request"
        verbose_name_plural = "Contact Requests"