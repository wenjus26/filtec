import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# Load environmental variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-filtec-super-secret-key-change-in-prod')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [host.strip() for host in os.environ.get('ALLOWED_HOSTS', '*').split(',') if host]

# ─── CSRF Trusted Origins (required when behind Nginx reverse proxy) ──────────
# Tells Django which domains are allowed to submit forms / AJAX POST requests.
# Must include the full scheme (https:// or http://)
_csrf_origins = os.environ.get(
    'CSRF_TRUSTED_ORIGINS',
    'http://localhost,http://127.0.0.1,http://web.filtec.in,https://web.filtec.in'
)
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_origins.split(',') if o.strip()]

# ─── Reverse Proxy Headers ────────────────────────────────────────────────────
# Tell Django to trust the X-Forwarded-Proto header from Nginx
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Application definition
INSTALLED_APPS = [
    # Jazzmin UI theme (must be placed before django.contrib.admin)
    'jazzmin',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party packages
    'ckeditor',
    'ckeditor_uploader',
    
    # Local apps
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'filtec_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.catalog_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'filtec_site.wsgi.application'

# Database Selection
# Priority:
# 1. DATABASE_URL env variable (Standard Docker / Heroku config)
# 2. Configured DB_ENGINE variable (sqlite, mysql, postgresql)
# 3. Fallback to default SQLite
DATABASES = {}

db_url = os.environ.get('DATABASE_URL')
if db_url:
    DATABASES['default'] = dj_database_url.config(default=db_url, conn_max_age=600)
else:
    db_engine = os.environ.get('DB_ENGINE', 'sqlite').lower()
    db_name = os.environ.get('DB_NAME', 'db.sqlite3')
    
    if db_engine == 'postgresql':
        DATABASES['default'] = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': db_name,
            'USER': os.environ.get('DB_USER', ''),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    elif db_engine == 'mysql':
        DATABASES['default'] = {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': db_name,
            'USER': os.environ.get('DB_USER', ''),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '3306'),
        }
    else:
        # Standard Fallback: SQLite
        DATABASES['default'] = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / db_name,
        }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media Files (User-uploaded assets)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# CKEditor Configuration
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}

# Jazzmin Configuration (Customizing Django Admin UI/UX)
JAZZMIN_SETTINGS = {
    "site_title": "FILTEC Admin",
    "site_header": "FILTEC Admin Portal",
    "site_brand": "FILTEC Polyplast",
    "site_logo": "images/logo.png",
    "login_logo": None,
    "welcome_sign": "Welcome to FILTEC Polyplast Admin Portal",
    "search_model": ["core.Product", "core.Event"],
    "show_sidebar": True,
    "navigation_expanded": True,
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Site", "url": "/", "new_window": True},
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.group": "fas fa-users",
        "core.Product": "fas fa-cubes",
        "core.Event": "fas fa-calendar-alt",
        "core.EventImage": "fas fa-images",
        "core.ContactSubmission": "fas fa-envelope",
        "core.PartnerApplication": "fas fa-handshake",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "changeform_format": "horizontal_tabs",
    "custom_css": "css/custom_admin.css",
}

JAZZMIN_UI_TWEAKS = {
    "navbar_theme": "navbar-danger navbar-dark",
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-danger",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
