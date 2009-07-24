from django.db import models

# Create your models here.
class TestModel(models.Model):
    whatever = models.CharField(blank=True, max_length=80)
    
    def __unicode__(self):
        return self.link
    
    def get_absolute_url(self):
        return "/%s" % self.id