from pathlib import Path
import os
import dj_database_url

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------
# Load .env file (local only)
# --------------------------------
def load_env():
    env_file = os.path.join(BASE_DIR, '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split('=', 1)
                    os.environ[key] = value

load_env()

# --------------------------------
# Core Django Settings
# --------------------------------

SECRET_KEY = os.getenv('SECRET_KEY', 'insecure-key')
DEBUG = os.getenv('DEBUG') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# --------------------------------
# Installed Apps
# --------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_recaptcha',
    'ckeditor',

    # Your apps
    'apps.lang',
    'apps.settings',
    'apps.homepage',
    'apps.aboutpage',
    'apps.portfoliopage',
    'apps.pricingpage',
    'apps.servicepage',
    'apps.blog',
    'apps.contactpage',
    'apps.adminapp',
    'apps.crm',
    'apps.hrm',
    'apps.userapp',
    'apps.legals',
    'apps.authapp',
    'apps.reports',
    'apps.marketing',
    'apps.custompage',
    'apps.order',
    'apps.ai',
    'apps.analytics',
]

# --------------------------------
# Middleware
# --------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.middleware.SlugDecodeMiddleware',
]

if os.getenv('DEMO_MODE') == 'True':
    MIDDLEWARE.append('core.middleware.middleware.DemoModeMiddleware')

if os.getenv("WHITENOISE_CONFIG") == "True":
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

ROOT_URLCONF = 'core.urls'

# --------------------------------
# Templates
# --------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # Custom context processors
                'core.context_processors.website_settings_context',
                'core.context_processors.promo_banner_context',
                'core.context_processors.seo_settings_context',
                'core.context_processors.menu_context',
                'core.context_processors.header_footer_context',
                'core.context_processors.user_profile_context',
                'core.context_processors.project_context',
                'core.context_processors.service_context',
                'core.context_processors.unsolved_tickets_context',
                'core.context_processors.demo_mode_enabled',
                'core.context_processors.notification_context',
                'core.context_processors.language_context',
                'apps.order.order_context.user_cart_context',
                'apps.settings.payment_method_context.payment_method_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# --------------------------------
# Email
# --------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') == "True"
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# --------------------------------
# DATABASE (Railway DATABASE_URL)
# --------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    print("⚠️ WARNING: No DATABASE_URL set. Using SQLite.")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

print("DATABASE CONFIG →", DATABASES)

# --------------------------------
# Passwords
# --------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --------------------------------
# Internationalization
# --------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.getenv('TIME_ZONE', 'UTC')
USE_I18N = True
USE_TZ = True

print(f"TIME_ZONE set to → {TIME_ZONE}")

# --------------------------------
# Static / Media Files
# --------------------------------

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, os.getenv('MEDIA_ROOT', 'media'))

if os.getenv("WHITENOISE_CONFIG") == "True":
    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

# --------------------------------
# Misc Settings
# --------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'authapp.User'

CKEDITOR_CONFIGS = {
    'default': {
        'height': '100%',
        'width': '100%',
    }
}

RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')

ENABLE_ARABIC_SIGNALS = False
ENABLE_BANGLA_SIGNALS = False
