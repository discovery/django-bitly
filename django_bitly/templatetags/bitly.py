from django.template import Library

from django_bitly.models import Bittle

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
    except AttributeError:
        # Fail silently
        pass
        
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
    except:
        pass

@register.filter
def referrers(value):
    """
    Save as clicks filter but returns list of Referrer objects rather than
    number of clicks.
    """
    
    try:
        bittle = Bittle.objects.bitlify(value)
        if bittle:
            referrers = bittle.referrers
        else:
            referrers = None
            
        return referrers
    except:
        pass