from django.db import models

class Talk(models.Model):
    GENDER_CHOICES = ((u'M', u'Male'), (u'F', u'Female'),)
    TYPE_CHOICES = (
            (u'GC', u'General Conference'), 
            (u'CES', u'CES Fireside'),
            (u'BYU', u'BYU Devotional'), 
            (u'CM', u'Church Magazine Article'),
            (u'RS', u'General Relief Society Meeting'),
            (u'YW', u'General Young Women Meeting'),
            )

    speaker = models.CharField(max_length=100)
    calling = models.CharField(max_length=100)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    date = models.DateField('Date given')
    title = models.CharField(max_length=500, blank=True)
    text = models.TextField()
    topic = models.CharField(max_length=500, blank=True)
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)

    def __unicode__(self):
        return self.title+', '+self.speaker


# Create your models here.
