from django.db import models
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
from django.utils import simplejson as json

import urllib, urllib2, datetime

# Create your models here.
class StringHolder(models.Model):
    """
    A helper model that allows you to create a Bittle with just a URL in a
    string rather than a Django object defining get_absolute_url().
    """
    absolute_url = models.URLField(verify_exists=True)
    
    def __unicode__(self):
        return u"StringHolder object for %s" % self.absolute_url
    
    def get_absolute_url(self):
        return self.absolute_url

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
        
        if isinstance(obj, basestring):
            obj, created = StringHolder.objects.get_or_create(absolute_url=obj)
                
        # If the object does not have a get_absolute_url() method or the
        # Bit.ly API authentication settings are not in settings.py, fail.
        if not (hasattr(obj, 'get_absolute_url') and settings.BITLY_LOGIN and settings.BITLY_API_KEY):
            print "Object '%s' does not have a 'get_absolute_url' method." % obj.__unicode__()
            return False
            
        current_domain = Site.objects.get_current().domain
        url = "http://%s%s" % (current_domain, obj.get_absolute_url())

        try:
            content_type = ContentType.objects.get_for_model(obj)
            bittle = Bittle.objects.get(content_type=content_type, object_id=obj.id)
        
            # Check if the absolute_url for the object has changed.
            if bittle.absolute_url != url:
                # If Django redirects are enabled and set up a redirect from
                # the old absolute url to the new one. Old Bittle should be
                # kept so that we still have access to its stats, but that
                # will mean handling multiple Bittles for any given object.
                # For now we'll delete the old Bittle and create a new one.
                bittle.delete()
                bittle = Bittle.objects.bitlify(obj)
                
            return bittle
        except:
            pass
        
        create_api = 'http://api.bit.ly/shorten'
        data = urllib.urlencode(dict(version="2.0.1", longUrl=url, login=settings.BITLY_LOGIN, apiKey=settings.BITLY_API_KEY, history=1))
        link = json.loads(urllib2.urlopen(create_api, data=data).read().strip())
        
        if link["errorCode"] == 0 and link["statusCode"] == "OK":
            results = link["results"][url]
            bittle = Bittle(content_object=obj, absolute_url=url, hash=results["hash"], shortKeywordUrl=results["shortKeywordUrl"], shortUrl=results["shortUrl"], userHash=results["userHash"])
            bittle.save()
            return bittle
        else:
            print "Failed secondary: %s" % link
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
    
    statstring = models.TextField(blank=True, editable=False)
    statstamp = models.DateTimeField(blank=True, null=True, editable=False)
    
    # Timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-date_created",]
    
    def __unicode__(self):
        return self.hash
        
    def _get_stats(self):
        now = datetime.datetime.now()
        stamp = self.statstamp
        timeout = datetime.timedelta(minutes=30)
        if stamp is None or now-stamp > timeout:
            create_api = "http://api.bit.ly/stats"
            data = urllib.urlencode(dict(version="2.0.1", hash=self.hash, login=settings.BITLY_LOGIN, apiKey=settings.BITLY_API_KEY))
            link = urllib2.urlopen(create_api, data=data).read().strip()
            self.statstring = link
            self.statstamp = now
            self.save()

        return json.loads(self.statstring)["results"]
    stats = property(_get_stats)
    
    def _get_clicks(self):
        return self.stats["clicks"]
    clicks = property(_get_clicks)
    
    def _get_referrers(self):
        class Referrer:
            domain = ""
            links = []
            
            def __init__(self, domain, links):
                self.domain = domain
                self.links = [(url, links[url]) for url in links]
            
            def __unicode__(self):
                if self.domain == "" and self.links[0][0] == "direct":
                    return "direct"
                elif self.domain != "":
                    return self.domain
        
        referrers = self.stats["referrers"]
        referrer_list = [Referrer(domain, referrers[domain]) for domain in referrers]
        return referrer_list
    referrers = property(_get_referrers)

    @models.permalink
    def get_absolute_url(self):
        return ('bittle', [self.id])