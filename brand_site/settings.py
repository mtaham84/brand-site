from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ۱. کلید امنیتی – از متغیر محیطی بخواند، در غیر این صورت یک کلید پیش‌فرض برای لوکال
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-for-local')

# ۲. حالت Debug – در لوکال True (اگر متغیر محیطی نبود)، روی سرور False
DEBUG = True

# ۳. هاست‌های مجاز – همیشه localhost را بپذیرد؛ اگر دامنه‌ای تنظیم شده باشد، آن را هم اضافه کند
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "raykashimisaba.com",
    "www.raykashimisaba.com"
]
CSRF_TRUSTED_ORIGINS = [
    "https://raykashimisaba.com",
    "https://www.raykashimisaba.com",
]
CSRF_COOKIE_SECURE = True


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
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

# ۴. دیتابیس – SQLite پیش‌فرض (برای لوکال)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# اگر متغیر محیطی DB_HOST وجود داشت (یعنی روی سرور هستیم)، به PostgreSQL سوئیچ کن
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
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': 'auto',
    },
}