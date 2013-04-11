from django.conf.urls.defaults import *
from django.views.generic import ListView, DetailView
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
    ('^admin/', include(admin.site.urls)),
    
    (r'^$', ListView.as_view(**object_dict)),
    url(r'^(?P<pk>\w+)/$', DetailView.as_view(**object_dict), name="test"),
)
