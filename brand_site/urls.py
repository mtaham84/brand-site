from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # زبان گزین
]

urlpatterns += i18n_patterns(
    path('sr8405/', admin.site.urls),
    path('', include('brands.urls')),
    path('catalog/', lambda request: redirect('/')),
    path('catalog', lambda request: redirect('/')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)