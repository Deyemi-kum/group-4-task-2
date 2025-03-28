import os

DJANGO_USER = os.getenv('DJANGO_USER', 'default_user')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webapp',  # Ensure this line is present
]

DEBUG = True  # Ensure this is True during development
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']  # Add this line
