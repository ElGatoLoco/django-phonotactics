from __future__ import unicode_literals

from django.db import models

class Word(models.Model):
    word = models.CharField(max_length=255)

    def __unicode__(self):
        return self.word
