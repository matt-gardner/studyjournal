from django.db import models
from datetime import date
from django.utils.safestring import SafeString

class Person(models.Model):
    GENDER_CHOICES = ((u'M', u'Male'), (u'F', u'Female'),)

    name = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)

    def callings(self):
        string = ''
        for calling in self.calling_set.all():
            string += calling.calling+', '
        return string[:-2]

    def get_calling(self, date):
        for calling in self.calling_set.all():
            if not calling.enddate:
                enddate = date.today()
            else:
                enddate = calling.enddate
            startdate = calling.startdate
            if date >= startdate and date <= enddate:
                return calling.calling
        else:
            raise ValueError(self.name+' did not have a calling on '+str(date))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Calling(models.Model):
    calling = models.CharField(max_length=100)
    startdate = models.DateField('Date Called')
    enddate = models.DateField('Date Released', null=True, blank=True)
    person = models.ForeignKey(Person)

    def __unicode__(self):
        return self.calling

    def pretty(self):
        if self.enddate:
            endstr = str(self.enddate)
        else:
            endstr = 'present'
        return self.calling+': '+str(self.startdate)+' - '+endstr


class Talk(models.Model):
    TYPE_CHOICES = (
            (u'GC', u'General Conference'), 
            (u'CES', u'CES Fireside'),
            (u'BYU', u'BYU Devotional'), 
            (u'CM', u'Church Magazine Article'),
            (u'RS', u'General Relief Society Meeting'),
            (u'YW', u'General Young Women Meeting'),
            )

    speaker = models.ForeignKey(Person)
    # If speaker is Other, this field is used
    speakername = models.CharField(max_length=100, blank=True)
    date = models.DateField('Date given')
    title = models.CharField(max_length=500, blank=True)
    text = models.TextField()
    topic = models.CharField(max_length=500, blank=True)
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)

    def __unicode__(self):
        if self.speakername:
            return self.title+', '+self.speakername
        else:
            return self.title+', '+self.speaker.name

    def pretty(self):
        return self.title+', '+str(self.date)+', '+self.type

    def htmltext(self):
        return SafeString('<p>'+self.text.replace('\n','</p><p>').encode('utf-8')+'</p>')


