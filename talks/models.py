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


class Person(models.Model):
    GENDER_CHOICES = ((u'M', u'Male'), (u'F', u'Female'),)

    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)

    def callings(self):
        string = ''
        for calling in self.calling_set.all():
            string += calling.calling+', '
        return string[:-2]

    def __unicode__(self):
        return self.name


class Calling(models.Model):
    calling = models.CharField(max_length=100)
    startdate = models.DateField('Date Called')
    enddate = models.DateField('Date Released', null=True, blank=True)
    person = models.ForeignKey(Person)

    def __unicode__(self):
        return self.calling

# Create your models here.
