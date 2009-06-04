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