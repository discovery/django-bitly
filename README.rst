Django Bitly
============

Bit.ly integration for django

A Django app that supports automatic generation and tracking of bit.ly hashes for objects on the site. Will automatically track changes to URLs, and, if necessary, maintain redirects for moved objects.

Requirements: Django 1.7+

Installation
------------

::

    $ pip install django-bitly

Add ``'django_bitly'`` to your ``INSTALLED_APPS``.

::

    $ django-admin.py syncdb

Define the following settings:

``BITLY_LOGIN``
   Your Bit.ly username
``BITLY_API_KEY``
   Your Bit.ly API Key

Usage
-----

Template Filters
~~~~~~~~~~~~~~~~
::

    {% load bitly %}

    {{ myobject|bitlify }}
    {{ myobject|clicks }}
    {{ myobject|referrers }}
    {{ myobject|referrer_chart:"250x100" }}

Available filters:

``bitlify``
    Gets or create a short URL for the passed object. If unable to get and/or create from bit.ly, will just return the object's ``get_absolute_url`` value.

``clicks``
    Returns the number of clicks that object has logged in bit.ly stats or fails silently.

``referrers``
    Same as ``clicks`` filter but returns list of Referrer objects rather than number of clicks.

``referrer_chart``
    Works like ``referrers``, but returns the URL for a Google charts pie chart.

Models
~~~~~~

You can use the ``bitlify`` manager method to create short urls for your model instances::

    >>> from django_bitly.models import Bittle
    >>> from myapp.models import MyModel
    
    >>> myobj = MyModel.objects.get(pk=1)
    >>> bittle = Bittle.objects.bitlify(myobj)
    >>> bittle.shortUrl
    'http://bit.ly/abcd1234'


Settings
--------

``BITLY_LOGIN``
    Your Bit.ly username. Required.
``BITLY_API_KEY``
    Your Bit.ly API Key. Required.
``BITLY_TIMEOUT``
    Timeout for the requests to Bit.ly, in seconds. Default: ``5``
