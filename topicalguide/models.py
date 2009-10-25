from django.db import models
from studyjournal.talks.models import Talk, Person
from scriptures import split_for_sorting

class Topic(models.Model):
    name = models.CharField(max_length=50)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    def talk_set(self):
        talk_set = []
        for entry in self.entry_set.all():
            talk_entry = None
            try:
                talk_entry = entry.talkentry
            except TalkEntry.DoesNotExist:
                continue
            if talk_entry:
                talk_set.append(talk_entry)
        talk_set.sort(key=lambda x: (x.talk.speaker.name(), x.talk.__unicode__()))
        return talk_set

    def scripture_set(self):
        scripture_set = []
        for entry in self.entry_set.all():
            scripture_entry = None
            try:
                scripture_entry = entry.scripturereferenceentry
            except ScriptureReferenceEntry.DoesNotExist:
                continue
            if scripture_entry:
                scripture_set.append(scripture_entry)
        scripture_set.sort(key=lambda x: split_for_sorting(x.reference))
        return scripture_set

    def num_entries(self):
        if len(self.entry_set.all()) == 1:
            return "1 entry"
        else:
            return "%d entries" % len(self.entry_set.all())

    def index_name(self):
        if self.name[:4] == 'The ':
            return self.name[4:]+', The'
        else:
            return self.name


class Entry(models.Model):
    topic = models.ForeignKey('Topic')
    notes = models.TextField(blank=True)


class TalkEntry(Entry):
    talk = models.ForeignKey('talks.Talk')
    quote = models.TextField(blank=True)

    def __unicode__(self):
        return self.talk.__unicode__()


class QuoteEntry(Entry):
    person = models.ForeignKey('talks.Person')
    quote = models.TextField()
    #source = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.person.__unicode__()


class ScriptureReferenceEntry(Entry):
    reference = models.CharField(max_length=50)

    def __unicode__(self):
        return self.reference
    

