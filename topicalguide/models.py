from django.db import models
from studyjournal.talks.models import Talk, Person
from scriptures import split_for_sorting, get_link
from django.utils.safestring import SafeString

class Topic(models.Model):
    name = models.CharField(max_length=50)
    subheading = models.CharField(max_length=100, blank=True)
    indexname = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    last_modified = models.DateTimeField()
    related_topics = models.ManyToManyField('Topic')

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    #def talk_set(self):
        #talk_set = []
        #for entry in self.entry_set.all():
            #talk_entry = None
            #try:
                #talk_entry = entry.talkentry
            #except TalkEntry.DoesNotExist:
                #continue
            #if talk_entry:
                #talk_set.append(talk_entry)
        #talk_set.sort(key=lambda x: (x.talk.speaker.name(), x.talk.__unicode__()))
        #return talk_set

    #def scripture_set(self):
        #scripture_set = []
        #for entry in self.entry_set.all():
            #scripture_entry = None
            #try:
                #scripture_entry = entry.scripturereferenceentry
            #except ScriptureReferenceEntry.DoesNotExist:
                #continue
            #if scripture_entry:
                #scripture_set.append(scripture_entry)
        #scripture_set.sort(key=lambda x: split_for_sorting(x.reference))
        #return scripture_set

    #def quote_set(self):
        #quote_set = []
        #for entry in self.entry_set.all():
            #quote_entry = None
            #try:
                #quote_entry = entry.quoteentry
                #quote_set.append(quote_entry)
            #except QuoteEntry.DoesNotExist:
                #pass
        #return quote_set

    def num_entries(self):
        return self.num_talks() + self.num_scriptures() + self.num_quotes()

    def num_talks(self):
        return len(self.talkentry_set.all())

    def num_scriptures(self):
        return len(self.scripturereferenceentry_set.all())

    def num_quotes(self):
        return len(self.quoteentry_set.all())

    def scripture_references(self):
        refs = list(self.scripturereferenceentry_set.all())
        refs.sort(key=lambda x: split_for_sorting(x.reference))
        return refs

    def index_name(self):
        if self.name[:4] == 'The ':
            return self.name[4:]+', The'
        else:
            return self.name


class TalkEntry(models.Model):
    topic = models.ForeignKey('Topic')
    notes = models.TextField(blank=True)
    talk = models.ForeignKey('talks.Talk')
    quote = models.TextField(blank=True)

    def __unicode__(self):
        return self.talk.__unicode__()


class QuoteEntry(models.Model):
    topic = models.ForeignKey('Topic')
    notes = models.TextField(blank=True)
    person = models.ForeignKey('talks.Person')
    quote = models.TextField()
    source = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.person.__unicode__()


class ScriptureReferenceEntry(models.Model):
    topic = models.ForeignKey('Topic')
    notes = models.TextField(blank=True)
    reference = models.CharField(max_length=50)

    def get_link(self):
        return SafeString(get_link(self.reference))

    def __unicode__(self):
        return self.reference
    

