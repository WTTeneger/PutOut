from lt.settings import *

ALLOWED_HOSTS = ['31.31.196.26', 'luckytrade.online', 'www.luckytrade.online']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'u1705556_luckytrader',
        'USER': 'u1705556_lt',
        'PASSWORD': 'jP0pK0dR6inG7o',
        'HOST': 'localhost',
    }
}
# DEBUG = False
print(BASE_DIR)
print(BASE_DIR.parent)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.parent / 'static/'
# STATIC_ROOT = 'static/'
