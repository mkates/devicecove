###########################################################################
#### Production Django Settings, local_settings overrides as neccesary ####
###########################################################################
#Old Main
DEBUG = False
TEMPLATE_DEBUG = DEBUG

import os

# General Admin
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
ADMINS = (
    ('Mitchell Kates', 'mhkates@gmail.com'),
    ('Mitchell Kates', 'mitch@vetcove.com'),
)
MANAGERS = ADMINS

LOGIN_URL = '/login'
LOGOUT_URL ="/"

from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "deviceapp.context_processors.basics",
)
# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.vetcove.com']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT=''
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

### Memcachier Cache Settings ################
def get_cache():
  import os
  try:
    os.environ['MEMCACHE_SERVERS'] = os.environ['MEMCACHIER_SERVERS'].replace(',', ';')
    os.environ['MEMCACHE_USERNAME'] = os.environ['MEMCACHIER_USERNAME']
    os.environ['MEMCACHE_PASSWORD'] = os.environ['MEMCACHIER_PASSWORD']
    return {
      'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'TIMEOUT': 500,
        'BINARY': True,
        'OPTIONS': { 'tcp_nodelay': True }
      }
    }
  except:
    return {
      'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
      }
    }

CACHES = get_cache()



# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
    #'django.contrib.staticfiles.finders.DefaultStorageFinder', # I removed this to get debug toolbar to work, if causes problems re-add it
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'k)1b(g&h8@hahwi*2a_@fu)3=4fnj4m8(i(0363pi(aa-&8mzg'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'deviceapp.middleware.SecureRequiredMiddleware.SecureRequiredMiddleware',
    'deviceapp.middleware.IEDetectionMiddleware.IEDetectionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)



ROOT_URLCONF = 'medapp.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'medapp.wsgi.application'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'boto', # For S3 File Storage
    'deviceapp', # Our sole app
    'south', #DB Migrations
    'imagekit', #For resizing images before S3 Upload
    'storages', #For file storage, works with S3
    'django_extensions',
    'password_reset', # Password reset app
    'djrill', #Django-Mandrill App
    'collectfast' #Used for quicker S3 Collectstatic (also fixes modified_time bug in s3 uploads)
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
try: #In try block because local settings cant import dj_database_url
    STATIC_URL = 'https://devicerock.s3.amazonaws.com/'
    HTTPS_SUPPORT = True
    import dj_database_url
    DATABASES = {
        "default": dj_database_url.config()
    }
    BALANCED_API_KEY = os.getenv("BALANCED_API_KEY") #Retrieves key from config variables
except Exception,e:
    print e
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
TEMPLATE_DIRS = (
     os.path.join(BASE_DIR, 'templates'),
)
#General settings
CONTACT_PHONE_NUMBER = 7325986434

#Amazon Credentials
# These are set in the heroku:config file only on the server

#Email Credentials
DEFAULT_FROM_EMAIL = 'info@vetcove.com'
SERVER_EMAIL = 'info@vetcove.com'

MANDRILL_API_KEY = "iSqtoSVWpB1aSTzA_YqaXg"
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
BALANCED_MARKETPLACE_ID = 'MP3D5qjr7obzojCvs5rfyK2Q'
# Amazon File Storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'devicerock'
AWS_PRELOAD_METADATA = True

# ImageKit File Storage
AWS_BUCKET_ = NAME = AWS_STORAGE_BUCKET_NAME 
IMAGEKIT_DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

### App Specific Variables ###
PAYOUT_WAIT_PERIOD = 14
CC_PROCESSING_FEE = .03

### Import the local settings ###
try:
    from local_settings import *
except ImportError:
    pass

    
