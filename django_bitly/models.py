import urllib, urllib2

from django.conf import settings
from django.db import models

# Create your models here.

# This should go into a manager like in django-registration
def bitlify(url):
    import simplejson as json
    
    create_api = 'http://api.bit.ly/shorten'
    data = urllib.urlencode(dict(version="2.0.1", longUrl=url, login=settings.BITLY_LOGIN, apiKey=settings.BITLY_API_KEY))
    link = urllib2.urlopen(create_api, data=data).read().strip()
    
    return json.loads(link)["results"][url]["shortUrl"]