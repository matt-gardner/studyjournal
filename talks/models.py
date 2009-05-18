from django.db import models
from datetime import date
from django.utils.safestring import SafeString


class Talk(models.Model):
    TYPE_CHOICES = (
            (u'GC', u'General Conference'), 
            (u'CES', u'CES Fireside'),
            (u'BYU', u'BYU Devotional'), 
            (u'CM', u'Church Magazine Article'),
            (u'RS', u'General Relief Society Meeting'),
            (u'YW', u'General Young Women Meeting'),
            )

    speaker = models.ForeignKey('Person')
    # If speaker is Other, this field is used
    speakername = models.CharField(max_length=100, blank=True)
    date = models.DateField('Date given')
    title = models.CharField(max_length=500, blank=True)
    text = models.TextField()
    topic = models.CharField(max_length=500, blank=True)
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    externallink = models.CharField(max_length=500, blank=True)

    def __unicode__(self):
        if self.speakername:
            return self.title+', '+self.speakername
        else:
            return self.title+', '+self.speaker.name()

    def pretty(self):
        return self.title+', '+str(self.date)+', '+self.type

    def htmltext(self):
        return SafeString('<p>'+\
                self.text.replace('\n','</p><p>').encode('utf-8')+'</p>')


class Person(models.Model):
    GENDER_CHOICES = ((u'M', u'Male'), (u'F', u'Female'),)

    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    suffix = models.CharField(max_length=10)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)

    def name(self):
        if self.middlename == '_':
            middlename = ' '
        else:
            middlename = ' '+self.middlename+' '
        if self.suffix == '_':
            suffix = ''
        else:
            suffix = ', '+self.suffix
        return self.firstname+middlename+self.lastname+suffix

    def callings(self):
        string = ''
        callings = []
        for calling in self.calling_set.all():
            if len(callings) == 0:
                callings.append(calling)
            else:
                for i in range(len(callings)):
                    if calling.startdate < callings[i].startdate:
                        callings.insert(i, calling)
                        break
                else:
                    callings.append(calling)
        for calling in callings:
            string += calling.__unicode__()+', '
        return string[:-2]

    def numtalks(self):
        return str(len(Talk.objects.filter(speaker=self.id)))
    numtalks.short_description='Number of Talks'

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
            raise ValueError(self.name()+\
                    ' did not have a calling on '+str(date))

    def __unicode__(self):
        return self.name()

    class Meta:
        ordering = ['lastname', 'firstname']
        verbose_name_plural = 'People'


class Calling(models.Model):
    CALLING_CHOICES = (
            (u'P',u'President of the Church'),
            (u'FC',u'First Counselor in the First Presidency'),
            (u'SC',u'Second Counselor in the First Presidency'),
            (u'C',u'Counselor in the First Presidency'),
            (u'A',u'Apostle'),
            (u'AT',u'Assistant to the Twelve'),
            (u'S',u'Seventy'),
            (u'B',u'Presiding Bishop'),
            (u'PB',u'Presiding Bishopric'),
            (u'O',u'Other'),
            )
    calling = models.CharField(max_length=4, choices=CALLING_CHOICES)
    # If calling is Other, this field is used
    othername = models.CharField(max_length=100, null=True, blank=True)
    startdate = models.DateField('Date Called')
    enddate = models.DateField('Date Released', null=True, blank=True)
    person = models.ForeignKey(Person)

    def __unicode__(self):
        if self.calling == 'O':
            return self.othername
        else:
            return self.get_calling_display()

    def pretty(self):
        if self.enddate:
            endstr = str(self.enddate)
        else:
            endstr = 'present'
        return self.__unicode__()+': '+str(self.startdate)+' - '+endstr




