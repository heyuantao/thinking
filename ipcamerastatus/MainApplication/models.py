from django.db import models

# Create your models here.
#class KeyValueStorage(models.Model):
#    key = models.CharField(max_length=500)
#    value = models.TextField(blank = True)
    
class ChannelModel(models.Model):
    description = models.CharField(max_length=500)
    url = models.TextField() 
