from django.conf import settings

BITLY_TIMEOUT = getattr(settings, 'BITLY_TIMEOUT', 5)
