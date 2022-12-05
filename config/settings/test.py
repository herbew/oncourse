"""
With these settings, tests run faster.
"""

from .base import *  
from .base import env
DATABASES = {
    'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': ':memory:',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_oncourse',
        'USER': 'uoncourse',
        'TEST': {
             'MIRROR': 'default',
         },
        'PASSWORD': 'PwDoncourseSatu1Dua3',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY", default="QNMVFsZxtD8aMdQdtZRlF6WIkEiMLfoPZ5p6fVXiepPCKRGTOTIlZQRXCCvOE0hX")
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": ""
    }
}

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG  
TEMPLATES[0]["OPTIONS"]["loaders"] = [  
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = "localhost"
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 1025

# Your stuff...
# ------------------------------------------------------------------------------
