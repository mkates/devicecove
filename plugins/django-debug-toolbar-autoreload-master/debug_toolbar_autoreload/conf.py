from django.conf import settings


DEBUG_TOOLBAR_CONFIG = getattr(settings, 'DEBUG_TOOLBAR_CONFIG', {})

AUTORELOAD_ENABLED = DEBUG_TOOLBAR_CONFIG.get('AUTORELOAD_ENABLED', True)
AUTORELOAD_FILETYPES = DEBUG_TOOLBAR_CONFIG.get(
    'AUTORELOAD_FILETYPES',
    ('template', 'css', 'js'))

AUTORELOAD_TIMEOUT = DEBUG_TOOLBAR_CONFIG.get('AUTORELOAD_TIMEOUT', None)
