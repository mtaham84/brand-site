from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ۱. کلید امنیتی – از متغیر محیطی بخواند (روی لوکال همان مقدار پیش‌فرض)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-6o$h&20+f2w&d_84wzcl_(ak6j6_p2*6x#3ib1)z=(1l%#f27n')

# ۲. حالت Debug – روی لوکال True (با متغیر محیطی خاموش)
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ۳. هاست‌های مجاز – روی لوکال فقط localhost
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'brands',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'brand_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'brands.context_processors.language_processor',
                'brands.context_processors.header_brands',
            ],
        },
    },
]

WSGI_APPLICATION = 'brand_site.wsgi.application'

# ۴. دیتابیس – SQLite پیش‌فرض، اما PostgreSQL اگر DB_HOST تنظیم باشد
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if os.environ.get('DB_HOST'):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'brandcenter'),
        'USER': os.environ.get('DB_USER', 'branduser'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('en', 'English'),
    ('fa', 'Persian'),
]
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ۵. فایل‌های Static و Media
STATIC_URL = '/static/'          # اسلش اول فراموش نشود
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')   # جدا از پوشه media قدیمی

# ۶. (اختیاری) اگر خواستید Object Storage داشته باشید، این بخش بعداً فعال می‌شود
# if os.environ.get('AWS_ACCESS_KEY_ID'):
#     INSTALLED_APPS.append('storages')
#     DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#     AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
#     AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
#     AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
#     AWS_S3_ENDPOINT_URL = os.environ['AWS_S3_ENDPOINT_URL']
#     AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'ir-thr')
#     AWS_DEFAULT_ACL = 'public-read'
#     AWS_QUERYSTRING_AUTH = False