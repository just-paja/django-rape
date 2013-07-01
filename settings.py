import os
from django.conf import settings

ROOT = getattr(settings, 'ROOT', os.path.abspath(os.path.dirname(__file__) + "/.."))

RAPED_SCRIPTS = getattr(settings, 'RAPED_SCRIPTS', {})

RAPED_STYLES = getattr(settings, 'RAPED_STYLES', {})

RAPE_PACK = getattr(settings, 'RAPE_PACK', False)

RAPE_SERIAL = getattr(settings, 'RAPE_SERIAL', 1)

RAPE_PATH = getattr(settings, 'RAPE_PATH', '%s/rape' % settings.ROOT)

settings.PROJECT_NAME = getattr(settings, 'PROJECT_NAME')

STATIC_ROOT = getattr(settings, 'STATIC_ROOT')
STATIC_URL = getattr(settings, 'STATIC_URL')
