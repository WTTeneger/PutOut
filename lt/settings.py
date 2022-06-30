import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from password_strength import PasswordPolicy  # , PasswordStats
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-n5rn4p50tq_nv63%0vt+3w@n4_l*r$qx+dgy=x+&8(%(r95fv2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Password
POLICY = PasswordPolicy.from_names(
    length=8,  # Минимальная длина
    uppercase=1,  # Минимум одна буква в верхнем регистре
    numbers=1,  # Минимум одна цифра
    special=1  # Минимум один спец символ
    # strength=0.3
)
PASSWORD_STRENGTH = 0.3
# EMAIL
EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST = 'mail.hosting.reg.ru'
# EMAIL_HOST_USER = 'main@lucky-trader.online'
# EMAIL_HOST_USER = 'connect@luckytrade.online'
# EMAIL_HOST_PASSWORD = 'oN4lK2qX7a'
# EMAIL_HOST_PASSWORD = 'kX7qX5hU1n'
# DEFAULT_FROM_EMAIL = 'main@lucky-trader.online'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
ACCOUNT_ACTIVATION_DAYS = 3
EMAIL_HOST = 'mail.hosting.reg.ru'
EMAIL_HOST_USER = 'connect@luckytrade.online'
DEFAULT_FROM_EMAIL = 'connect@luckytrade.online'
EMAIL_HOST_PASSWORD = 'kX7qX5hU1n'
EMAIL_PORT = 587
# EMAIL_USE_SSL = True

# EMAIL_USE_TLS = False

# SERVER_EMAIL    = 'root@my-domain.com'
#

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'rest_framework',
    'colorfield',
    'solo',
    'sslserver',
    'rest_framework_simplejwt',
    # 'django_celery_beat',
    # 'compressor',
]

INSTALLED_APPS += [
    'core.main',
    # 'core.api',
    # 'core.app',
    'admin_reorder',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # 'user_language_middleware.UserLanguageMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

# STATICFILES_FINDERS = [
#     'compressor.finders.CompressorFinder'
# ]
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

ADMIN_REORDER = (
    # First group
    {'app': 'main',
     'label': 'Пользовательские',
     'models': ('main.UserData',
                'main.Client',
                'main.Trader',
                'auth.User',
                )
     },
    {'app': 'main',
     'label': 'Вторичная',
     'models': ('main.Orders',
                'main.APIKeys',
                'main.TelegramAccount',
                'main.Referral',
                'main.Subscriptions',
                'main.TwoFA',
                )
     },
    {'app': 'main',
     'label': 'Продукты',
     'models': ('main.Course',
                'main.Lesson',
                'main.Product',
                'main.ProductLogs',
                'main.ProductOrders',
                'main.Transactions',
                )
     },
    {'app': 'main',
     'label': 'Система',
     'models': ('main.SiteConfiguration',
                'main.Logs',
                'main.ReferralLogs',
                'main.VerifyEmail',
                'main.TelegramAccount'
                )
     },
    # Second group: same app, but different label
    # {'app': 'myapp', 'label': 'Group2',
    #  'models': ('myapp.Model_2',
    #             'myapp.Model_3',)
    #  },
)

ROOT_URLCONF = 'lt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
            'libraries': {
                'staticfiles': 'django.templatetags.static',
                # 'main_static': 'lt.static.css',
            }
        },
    },
]

WSGI_APPLICATION = 'lt.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
# LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'  # 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'

locale = False
if locale:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LANGUAGES = (
    ('en', _('Английский')),
    ('ru', _('Русский')),
    ('fr', _('Французкий')),
    ('uk', _('Украинский')),
    ('de', _('Немецкий')),
    ('ja', _('Японский')),
    ('zh', _('Китайский')),
    ('id', _('Индонезийский')),
    ('pt', _('Португальский')),
    ('es', _('Испанский')),
    ('th', _('Тайский')),
    ('ar', _('Арабский')),
    # ('id', _('Индонезийский')),
)

# Сделать языки
# Китай >
# Индонезия >
# Япиния >
# Португалия >
# Испания >
# Тайский >
# Арабский

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Yandex Translator
YT_folder_id = 'b1go1se704oksj8108ec'
YT_OAuth = 'AQAAAAAZBZq2AATuwUwrJc019UsZt1vM6Z4XobI'

# TG id Admin
ADMINTGID = 569452912  # 420624020

# settings site
PAY_CARD = True

HOST_ADDRESS = '127.0.0.1:8000'
# HOST_ADDRESS = 'luckytrade.online'