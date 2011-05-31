from django.db import models
import datetime
from django.utils.safestring import SafeString


class Talk(models.Model):
    TYPE_CHOICES = (
            (u'GC', u'General Conference'), 
            (u'CES', u'CES Fireside'),
            (u'BYU', u'BYU Devotional'), 
            (u'BYUI', u'BYU-Idaho Devotional'),
            (u'CM', u'Church Magazine Article'),
            (u'RS', u'General Relief Society Meeting'),
            (u'YW', u'General Young Women Meeting'),
            (u'O', u'Other'),
            )

    speaker = models.ForeignKey('Person')
    # If speaker is Other, this field is used (soon to be removed...)
    speakername = models.CharField(max_length=100, blank=True)
    date = models.DateField('Date given')
    title = models.CharField(max_length=500, blank=True)
    text = models.TextField()
    topic = models.CharField(max_length=500, blank=True)
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    externallink = models.CharField(max_length=500, blank=True)
    # This is looking forward, in case I want to download all of the audio
    # files (which I'm currently debating)
    audiofile = models.CharField(max_length=500, blank=True)
    audiolink = models.CharField(max_length=500, blank=True)

    def __unicode__(self):
        if self.speakername:
            return self.title+', '+self.speakername
        else:
            return self.title+', '+self.speaker.name()

    def pretty(self):
        return self.title+', '+str(self.date)+', '+self.type

    def date_string(self):
        return str(self.date)

    def get_rating(self):
        ratings = self.rating_set.all()
        if ratings:
            average = sum([int(r.rating) for r in ratings])/len(ratings)
            return '%d (%d)' % (average, len(ratings))
        else:
            return 'No ratings'


class Rating(models.Model):
    RATING_CHOICES = (
            (u'1', u'1'),
            (u'2', u'2'),
            (u'3', u'3'),
            (u'4', u'4'),
            (u'5', u'5'),
            )

    talk = models.ForeignKey('Talk')
    user = models.ForeignKey('auth.User')
    rating = models.CharField(max_length=1, choices=RATING_CHOICES)
    comment = models.TextField()


class Person(models.Model):
    GENDER_CHOICES = ((u'M', u'Male'), (u'F', u'Female'),)

    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    suffix = models.CharField(max_length=10)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    wikipedia_bio = models.CharField(max_length=1000, blank=True)
    ga_bio = models.CharField(max_length=1000, blank=True)

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
        return ', '.join([x.__unicode__() for x in callings])

    def get_calling(self, date):
        for calling in self.calling_set.all():
            if not calling.enddate:
                enddate = datetime.date.today()
            else:
                enddate = calling.enddate
            startdate = calling.startdate
            if startdate <= date <= enddate:
                return calling.calling
        else:
            raise ValueError(self.name()+\
                    ' did not have a calling on '+str(date))

    def numtalks(self):
        return str(len(self.talk_set.all()))
    numtalks.short_description='Number of Talks'

    def __unicode__(self):
        return self.name()

    def average_rating(self):
        ratings = []
        for talk in self.talk_set.all():
            for rating in talk.rating_set.all():
                ratings.append(int(rating.rating))
        if not ratings:
            return 'No ratings'
        num = len(ratings)
        average = float(sum(ratings)) / num
        if average % 1 == 0.0:
            return '%d (with %d ratings)' % (average, num)
        else:
            return '%.1f (with %d ratings)' % (average, num)

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
            (u'PS',u'Presidency of the Seventy'),
            (u'1S',u'First Quorum of the Seventy'),
            (u'2S',u'Second Quorum of the Seventy'),
            (u'AS',u'Area Seventy'),
            (u'PB',u'Presiding Bishop'),
            (u'PBRC',u'Presiding Bishopric'),
            (u'RSP',u'Relief Society General President'),
            (u'RSC',u'Relief Society General Presidency'),
            (u'YWP',u'Young Women General President'),
            (u'YWC',u'Young Women General Presidency'),
            (u'YMP',u'Young Men General President'),
            (u'YMC',u'Young Men General Presidency'),
            (u'SSP',u'Sunday School General President'),
            (u'SSC',u'Sunday School General Presidency'),
            (u'PC',u'Patriarch of the Church'),
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




