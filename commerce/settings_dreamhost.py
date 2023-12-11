from .settings import *


ALLOWED_HOSTS = ['deals.uaa490.org', 'www.deals.uaa490.org']
DEBUG=False

STATIC_ROOT = '/home/deals490/deals.uaa490.org/public/static/'
MEDIA_ROOT = '/home/deals490/deals.uaa490.org/public/media/'

import environ
env = environ.Env()
environ.Env.read_env()

DATABASES = {
    'default': {
	'ENGINE': 'django.db.backends.mysql',
    'NAME': env('DATABASE_NAME'),
    'USER': env('DATABASE_USER'),
    'PASSWORD': env('DATABASE_PASSWORD'),
	'HOST': 'mysql.deals.uaa490.org',
	'PORT': '3306',
    }
}

