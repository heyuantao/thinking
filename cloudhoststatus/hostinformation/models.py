from __future__ import unicode_literals

from django.db import models

# Create your models here.
class KeyValueStorage(models.Model):
    key = models.CharField(max_length=500)
    value = models.TextField(blank = True)
