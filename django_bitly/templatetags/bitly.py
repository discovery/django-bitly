from django.template import Library

from django_bitly.models import Bittle
from django_bitly.exceptions import BittleException

import urllib

register = Library()


@register.filter
def bitlify(value):
    """
    Gets or create a Bittle object for the passed object. If unable to get
    Bittle and/or create bit.ly, will just return the get_absolute_url value.
    """

    try:
        bittle = Bittle.objects.bitlify(value)
        if bittle:
            url = bittle.shortUrl
        else:
            url = value.get_absolute_url
        return url
    except (BittleException, Bittle.DoesNotExist):
        return value.get_absolute_url()


@register.filter
def clicks(value):
    """
    Retrieves Bittle object for passed object, or fails silently. Returns the
    number of clicks that object has logged in bit.ly stats.
    """
    try:
        bittle = Bittle.objects.bitlify(value)
        if bittle:
            clicks = bittle.clicks
        else:
            clicks = "n/a"
        return clicks
    except Bittle.DoesNotExist:
        pass


@register.filter
def referrers(value):
    """
    Same as clicks filter but returns list of Referrer objects rather than
    number of clicks.
    """
    try:
        bittle = Bittle.objects.bitlify(value)
        if bittle:
            referrers = bittle.referrers
        else:
            referrers = None

        return referrers
    except Bittle.DoesNotExist:
        pass


@register.filter
def referrer_chart(value, chs="250x100"):
    """
    Works like referrers, but returns the URL for a Google charts pie chart.
    http://chart.apis.google.com/chart?cht=p3&chd=t:60,40&chs=250x100&chl=Hello|World
    """

    try:
        bittle = Bittle.objects.bitlify(value)
        if bittle:
            referrers = bittle.referrers
            clicks = bittle.clicks
            cht = "p3"
            chd = []
            chl = []

            for referrer in referrers:
                count = 0
                for link in referrer.links:
                    count += link[1]
                perc = (1.0 * count / clicks) * 100
                chd.append("%s" % int(perc))
            chd = "t:%s" % ','.join(chd)

            for referrer in referrers:
                chl.append(referrer.__unicode__())
            chl = '|'.join(chl)

            google_api = "http://chart.apis.google.com/chart"
            data = urllib.urlencode(dict(cht=cht, chd=chd, chs=chs, chl=chl))
            referrers = "%s?%s" % (google_api, data)
        else:
            referrers = None

        return referrers
    except Bittle.DoesNotExist:
        pass
