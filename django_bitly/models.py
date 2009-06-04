from django.db import models
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# Create your models here.
class BittleManager(models.Manager):
    """
    Custom manager for the ``Bittle`` model.
    
    Defines methods to provide shortcuts for creation and management of
    Bit.ly links to local objects.
    """
    
    def bitlify(self, obj):
        """
        Creates a new ``Bittle`` object based on the object passed to it.
        The object must have a ``get_absolute_url`` in order for this to
        work.
        """
        import urllib, urllib2
        import simplejson as json
        from django.conf import settings
        
        if not (obj.get_absolute_url and settings.BITLY_LOGIN and settings.BITLY_API_KEY):
            # print "Failed initial"
            return False
        
        current_domain = Site.objects.get_current().domain
        url = "http://%s%s" % (current_domain, obj.get_absolute_url())
        
        create_api = 'http://api.bit.ly/shorten'
        data = urllib.urlencode(dict(version="2.0.1", longUrl=url, login=settings.BITLY_LOGIN, apiKey=settings.BITLY_API_KEY))
        link = json.loads(urllib2.urlopen(create_api, data=data).read().strip())
        
        if link["errorCode"] == 0 and link["statusCode"] == "OK":
            results = link["results"][url]
            bittle = Bittle(content_object=obj, absolute_url=url, hash=results["hash"], shortKeywordUrl=results["shortKeywordUrl"], shortUrl=results["shortUrl"], userHash=results["userHash"])
            bittle.save()
            return bittle
        else:
            # print "Failed secondary: %s" % link
            return False
    
class Bittle(models.Model):
    """An object representing a Bit.ly link to a local object."""
    
    objects = BittleManager()
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    absolute_url = models.URLField(verify_exists=True)
    
    hash = models.CharField(max_length=10)
    shortKeywordUrl = models.URLField(blank=True, verify_exists=True)
    shortUrl = models.URLField(verify_exists=True)
    userHash = models.CharField(max_length=10)
    
    def __unicode__(self):
        return u"Bittle"

    @models.permalink
    def get_absolute_url(self):
        return ('Bittle', [self.id])