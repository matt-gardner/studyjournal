from django.db import models
from scriptures import split_for_sorting, get_link
from django.utils.safestring import SafeString

class Topic(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('auth.User')
    subheading = models.CharField(max_length=100, blank=True)
    indexname = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    last_modified = models.DateTimeField()
    related_topics = models.ManyToManyField('Topic')

    class Meta:
        ordering = ['indexname']

    def __unicode__(self):
        return self.indexname + ' (' + self.user.first_name + ')'

    def num_entries(self):
        return self.num_talks() + self.num_scriptures() + self.num_quotes()

    def scripture_references(self):
        refs = list(self.reference_set.all())
        refs.sort(key=lambda x: split_for_sorting(x.reference))
        return refs


class TalkEntry(models.Model):
    topic = models.ForeignKey('Topic')
    notes = models.TextField(blank=True)
    talk = models.ForeignKey('talks.Talk')
    quote = models.TextField(blank=True)

    def __unicode__(self):
        return self.talk.__unicode__()


class Quote(models.Model):
    topic = models.ForeignKey('Topic')
    notes = models.TextField(blank=True)
    person = models.ForeignKey('talks.Person')
    quote = models.TextField()
    source = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.person.__unicode__()


class Reference(models.Model):
    topic = models.ForeignKey('Topic')
    notes = models.TextField(blank=True)
    reference = models.CharField(max_length=150)

    def get_link(self):
        return SafeString(get_link(self.reference))

    def __unicode__(self):
        return self.reference
    

