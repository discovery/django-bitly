import re
import urllib
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from datetime import timedelta
try:
    from django.utils import timezone as datetime
except ImportError:
    from datetime import datetime

from django.db import models
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
try:
    from django.utils import simplejson as json
except ImportError:
    import json

from .conf import BITLY_TIMEOUT
from .exceptions import BittleException


# Create your models here.
class StringHolder(models.Model):
    """
    A helper model that allows you to create a Bittle with just a URL in a
    string rather than a Django object defining get_absolute_url().
    """
    absolute_url = models.URLField()

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
    def filter_for_instance(self, obj):
        app_label = obj._meta.app_label
        model = obj._meta.module_name
        return self.filter(content_type__app_label=app_label, content_type__model=model, object_id=obj.pk)

    def get_for_instance(self, obj):
        try:
            return self.filter_for_instance(obj)[0]
        except IndexError:
            raise self.model.DoesNotExist

    def bitlify(self, obj, scheme='http'):
        """
        Creates a new ``Bittle`` object based on the object passed to it.
        The object must have a ``get_absolute_url`` in order for this to
        work.
        """

        if isinstance(obj, basestring):
            obj, created = StringHolder.objects.get_or_create(absolute_url=obj)

        # If the object does not have a get_absolute_url() method or the
        # Bit.ly API authentication settings are not in settings.py, fail.
        if not (settings.BITLY_LOGIN and settings.BITLY_API_KEY):
            raise BittleException("Bit.ly credentials not found in settings.")

        if not hasattr(obj, 'get_absolute_url'):
            raise BittleException("Object '%s' does not have a 'get_absolute_url' method."
                % obj.__unicode__())

        current_domain = Site.objects.get_current().domain

        obj_url = obj.get_absolute_url()
        if re.match(r'^(aim|apt|bitcoin|callto|cid|data|dav|fax|feed|geo|go|h323|iax|im|magnet|mailto|message|mid|msnim|mvn|news|palm|paparazzi|pres|proxy|query|session|sip|sips|skype|sms|spotify|steam|tag|tel|things|urn|uuid|view-source|ws|wyciwyg|xmpp|ymsgr):', obj_url, re.IGNORECASE):
            # These are the URI Schemes that can be legitimately used with no slashes:
            # http://en.wikipedia.org/wiki/URI_scheme
            # Treat these as ready-to-go
            url = obj_url
        elif re.match(r'(attachment|platform):/', obj_url, re.IGNORECASE):
            # These can be used with only one forward slash
            # Treat these as ready-to-go
            url = obj_url
        elif re.match(r'^https?://', obj_url, re.IGNORECASE):
            # This is an HTTP link, just send it through.
            url = obj_url
        elif re.match(r'^[^:/]+://', obj_url, re.IGNORECASE):
            # These are meant to be used with double-forward-slashes
            # Treat these as ready-to-go
            url = obj_url
        elif re.match(r'^//', obj_url, re.IGNORECASE):
            # If this is schemeless, fully-qualified URL, sometimes used to
            # avoid mixed-scheme webpage issues (particularly, http/https
            # security issues).  We'll need an actual scheme for this though,
            # so we'll use whatever they pass into the kwarg: scheme.
            url = "%s:%s" % (scheme, obj_url)
        else:
            # Normal, relative ("absolute" in Django-speak) URLs
            url = "%s://%s%s" % (scheme, current_domain, obj_url)

        try:
            bittle = Bittle.objects.get_for_instance(obj)

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
        except Bittle.DoesNotExist:
            pass

        create_api = 'http://api.bit.ly/shorten'
        data = urllib.urlencode(dict(version="2.0.1", longUrl=url, login=settings.BITLY_LOGIN, apiKey=settings.BITLY_API_KEY, history=1))
        link = json.loads(urllib2.urlopen(create_api, data=data, timeout=BITLY_TIMEOUT).read().strip())

        if link["errorCode"] == 0 and link["statusCode"] == "OK":
            results = link["results"][url]
            bittle = Bittle(content_object=obj, absolute_url=url, hash=results["hash"], shortKeywordUrl=results["shortKeywordUrl"], shortUrl=results["shortUrl"], userHash=results["userHash"])
            bittle.save()
            return bittle
        else:
            raise BittleException("Failed secondary: %s" % link)


class Bittle(models.Model):
    """An object representing a Bit.ly link to a local object."""
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    absolute_url = models.URLField()

    hash = models.CharField(max_length=10)
    shortKeywordUrl = models.URLField(blank=True)
    shortUrl = models.URLField()
    userHash = models.CharField(max_length=10)

    statstring = models.TextField(blank=True, editable=False)
    statstamp = models.DateTimeField(blank=True, null=True, editable=False)

    # Timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    objects = BittleManager()

    class Meta:
        ordering = ("-date_created",)

    def __unicode__(self):
        return self.hash

    def _get_stats(self):
        now = datetime.now()
        stamp = self.statstamp
        timeout = timedelta(minutes=30)
        if stamp is None or now - stamp > timeout:
            create_api = "http://api.bit.ly/stats"
            data = urllib.urlencode(dict(version="2.0.1", hash=self.hash, login=settings.BITLY_LOGIN, apiKey=settings.BITLY_API_KEY))
            link = urllib2.urlopen('%s?%s' % (create_api, data), timeout=BITLY_TIMEOUT).read().strip()
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
