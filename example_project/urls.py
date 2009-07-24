from django.conf.urls.defaults import *
from django.views.generic import list_detail
from testapp.models import TestModel

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

def get_objects():
    return TestModel.objects.all()
object_dict = {'queryset': get_objects()}

urlpatterns = patterns('',
    # Example:
    # (r'^example_project/', include('example_project.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    
    (r'^$', list_detail.object_list, object_dict),
    url(r'^(?P<object_id>\w+)/$', list_detail.object_detail, object_dict, name="test"),
)
