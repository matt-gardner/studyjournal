from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django import forms
from studyjournal.topicalguide.models import Topic, TalkEntry, Quote, Reference
from studyjournal.talks.models import Person, Talk
from datetime import datetime
from scriptures import get_book, split_for_sorting, books

def index(request):
    if 'delete' in request.GET:
        topic = Topic.objects.get(pk=request.GET['delete'])
        topic.delete()
        return HttpResponseRedirect('/topics')
    allowed_orderings = ['indexname', '-indexname', 'last_modified',
            '-last_modified']
    ordering = 'indexname'
    if 'order_by' in request.GET:
        ordering = request.GET['order_by']
    if ordering in allowed_orderings:
        topics = Topic.objects.order_by(ordering)
    else:
        topics = list(Topic.objects.all())
        if ordering == 'scriptures':
            topics.sort(key=lambda x:
                    (len(x.reference_set.all()), x.indexname))
        elif ordering == '-scriptures':
            topics.sort(key=lambda x:
                    (-len(x.reference_set.all()), x.indexname))
        elif ordering == 'talks':
            topics.sort(key=lambda x:
                    (len(x.talkentry_set.all()), x.indexname))
        elif ordering == '-talks':
            topics.sort(key=lambda x:
                    (-len(x.talkentry_set.all()), x.indexname))
        elif ordering == 'quotes':
            topics.sort(key=lambda x:
                    (len(x.quote_set.all()), x.indexname))
        elif ordering == '-quotes':
            topics.sort(key=lambda x:
                    (-len(x.quote_set.all()), x.indexname))
        elif ordering == 'user':
            topics.sort(key=lambda x:
                    (x.user.username, x.indexname))
        elif ordering == '-user':
            topics.sort(cmp=lambda x,y: -cmp(x[0],y[0]) if cmp(x[0], y[0])
                    else cmp(x[1], y[1]), key=lambda x:
                    (x.user.username, x.indexname))
    return render_to_response('topicalguide/index.html',
            {'topics' : topics, 'ordering': ordering})

def topic(request, topic_id):
    if 'delete' in request.GET:
        delete = request.GET['delete']
        if 'talk' in delete:
            talkentry = TalkEntry.objects.get(pk=delete[4:])
            talkentry.delete()
        elif 'sr' in delete:
            srentry = Reference.objects.get(pk=delete[2:])
            srentry.delete()
        elif 'q' in delete:
            qentry = Quote.objects.get(pk=delete[1:])
            qentry.delete()
        elif 'related' in delete:
            rt = Topic.objects.get(pk=delete[7:])
            topic = get_object_or_404(Topic, pk=topic_id)
            topic.related_topics.remove(rt)
            topic.save()
        return HttpResponseRedirect('/topic/'+topic_id)
    topic = get_object_or_404(Topic, pk=topic_id)
    return render_to_response('topicalguide/topic.html', {'topic' : topic})

def scriptures(request):
    scriptures = dict()
    for entry in Reference.objects.all():
        book = get_book(entry.reference)
        if book not in scriptures:
            scriptures[book] = []
        scriptures[book].append(entry)
    scripture_set = ScriptureSet()
    for book in books:
        if book in scriptures:
            scriptures[book].sort(key=lambda x: split_for_sorting(x.reference))
            b = Book(book)
            b.refs = scriptures[book]
            scripture_set.books.append(b)
    return render_to_response('topicalguide/scriptures.html',
            {'scriptures' : scripture_set})

def add_topic(request):
    error = False
    if request.POST:
        new_topic_form = AddTopicForm(request.POST)
        if new_topic_form.is_valid():
            new_topic_form.save()
            timestamp = request.POST['last_modified']
            date, time = timestamp.split()
            year, month, day = map(int, date.split('-'))
            hour, minute, second = map(int, time.split(':'))
            timestamp = datetime(year, month, day, hour, minute, second)
            new_topic = Topic.objects.get(last_modified=timestamp)
            return HttpResponseRedirect('/topic/'+str(new_topic.id))
        else:
            error = True
    page_vars = dict()
    if error:
        form = new_topic_form
        page_vars['header'] = "Error in adding topic! Please try again"
    else:
        form = AddTopicForm()
        page_vars['header'] = "Add a new topic"
    page_vars['form'] = form
    page_vars['submit_label'] = "Add topic"
    return render_to_response('add_form.html', page_vars)

def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.POST:
        form = AddTopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            topic.last_modified = datetime.now()
            topic.save()
        return HttpResponseRedirect('/topic/'+str(topic.id))
    form = AddTopicForm(instance=topic)
    page_vars = dict()
    page_vars['form'] = form
    page_vars['submit_label'] = "Edit topic"
    page_vars['header'] = "Edit topic " + topic.name
    return render_to_response('add_form.html', page_vars)


def add_related_topic(request, topic_id, **kwds):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.POST:
        related_topic = Topic.objects.get(pk=request.POST['related_topic'])
        if (related_topic not in topic.related_topics.all() and
                related_topic != topic):
            topic.related_topics.add(related_topic)
            topic.last_modified = datetime.now()
            topic.save()
        return HttpResponseRedirect('/topic/'+topic_id)
    page_vars = dict()
    form = RelatedTopicForm()
    page_vars['submit_label'] = "Add related topic"
    page_vars['header'] = "Add a related topic to " + topic.name
    page_vars['form'] = form
    return render_to_response('add_form.html', page_vars)


def add_scripture_entry(request, topic_id, **kwds):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.POST:
        if request.POST['edit'] != 'False':
            entry = Reference.objects.get(pk=request.POST['edit'])
            entry.notes = request.POST['notes'].strip()
            entry.reference = request.POST['reference']
        else:
            entry = Reference(
                    topic=topic,
                    notes=request.POST['notes'].strip(),
                    reference=request.POST['reference'],
                    )
        entry.save()
        topic.last_modified = datetime.now()
        topic.save()
        return HttpResponseRedirect('/topic/'+topic_id)
    page_vars = dict()
    if kwds.has_key('entry_id'):
        entry = Reference.objects.get(pk=kwds['entry_id'])
        form = AddScriptureForm(initial={'topic': topic.name,
                'notes': entry.notes,
                'reference': entry.reference,
                'edit': entry.id})
        page_vars['submit_label'] = "Edit reference"
        page_vars['header'] = "Edit a scripture reference in " + topic.name
    else:
        form = AddScriptureForm(initial={'topic': topic.name,
                'edit': 'False'})
        page_vars['submit_label'] = "Add reference"
        page_vars['header'] = "Add a scripture reference to " + topic.name
    page_vars['form'] = form
    return render_to_response('add_form.html', page_vars)

def add_talk_entry(request, topic_id, **kwds):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.POST and request.POST['edit'] != 'Person':
        if request.POST['edit'] != 'False':
            entry = TalkEntry.objects.get(pk=request.POST['edit'])
            entry.notes = request.POST['notes'].strip()
            entry.quote = request.POST['quote']
        else:
            entry = TalkEntry(
                    topic=topic,
                    notes=request.POST['notes'].strip(),
                    talk=Talk.objects.get(pk=request.POST['talk']),
                    quote=request.POST['quote'],
                    )
        entry.save()
        topic.last_modified = datetime.now()
        topic.save()
        return HttpResponseRedirect('/topic/'+topic_id)
    page_vars = dict()
    if request.POST:
        form = AddTalkForm(person=request.POST['talk'],
                initial={'topic': topic.name,
                'edit': 'False'})
        page_vars['submit_label'] = "Add Talk"
        page_vars['header'] = "Add a talk to " + topic.name
    elif kwds.has_key('entry_id'):
        entry = TalkEntry.objects.get(pk=kwds['entry_id'])
        form = AddTalkForm(edit=True, person=entry.talk.speaker.id,
                initial={'topic': topic.name,
                'talk': entry.talk.id,
                'quote': entry.quote,
                'notes': entry.notes,
                'edit': entry.id})
        page_vars['submit_label'] = "Edit talk"
        page_vars['header'] = "Edit a quote for a talk in " + topic.name
    else:
        form = AddTalkForm(initial={'topic': topic.name,
                'edit': 'Person'})
        page_vars['submit_label'] = "Select Talk"
        page_vars['header'] = "Add a talk to " + topic.name
        page_vars['subheader'] = "Pick a person first"
    page_vars['form'] = form
    return render_to_response('add_form.html', page_vars)

def add_quote(request, topic_id, **kwds):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.POST:
        if request.POST['edit'] != 'False':
            entry = Quote.objects.get(pk=request.POST['edit'])
            entry.person = Person.objects.get(pk=request.POST['person'])
            entry.quote = request.POST['quote']
            entry.source = request.POST['source']
        else:
            entry = Quote(
                    topic=topic,
                    person=Person.objects.get(pk=request.POST['person']),
                    quote=request.POST['quote'],
                    source=request.POST['source'],
                    notes=request.POST['notes'].strip(),
                    )
        entry.save()
        topic.last_modified = datetime.now()
        topic.save()
        return HttpResponseRedirect('/topic/'+topic_id)
    page_vars = dict()
    if kwds.has_key('entry_id'):
        entry = Quote.objects.get(pk=kwds['entry_id'])
        form = AddQuoteForm(initial={'topic': topic.name,
                'notes': entry.notes,
                'person': entry.person.id, # this doesn't work -- why not?
                'quote': entry.quote,
                'source': entry.source,
                'edit': entry.id})
        page_vars['submit_label'] = "Edit quote"
        page_vars['header'] = "Edit a quote in " + topic.name
    else:
        form = AddQuoteForm(initial={'topic': topic.name,
                'edit': 'False'})
        page_vars['submit_label'] = "Add quote"
        page_vars['header'] = "Add a quote to " + topic.name
    page_vars['form'] = form
    return render_to_response('add_form.html', page_vars)

class AddTopicForm(forms.ModelForm):
    def __init__(self, *args, **kwds):
        super(AddTopicForm, self).__init__(*args, **kwds)
        self.fields['last_modified'].widget = forms.HiddenInput()
        self.fields['last_modified'].initial = str(datetime.now()).split('.')[0]

    class Meta:
        model = Topic
        exclude = ['related_topics']

class AddScriptureForm(forms.ModelForm):
    topic = forms.CharField(label='Topic',
            widget=forms.TextInput({'readonly':True}))
    edit = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = Reference
        fields = ['topic','reference','notes']

class AddQuoteForm(forms.ModelForm):
    topic = forms.CharField(label='Topic',
            widget=forms.TextInput({'readonly':True}))
    edit = forms.CharField(widget=forms.HiddenInput())
    person = forms.ModelChoiceField(Person.objects.all(),
            label='Person', empty_label=None)
    class Meta:
        model = Quote
        fields = ['topic','person','quote','source','notes']

class AddTalkForm(forms.ModelForm):
    def __init__(self, edit=False, person=None, talk=None, *args, **kwds):
        super(AddTalkForm, self).__init__(*args, **kwds)
        if talk:
            return
        if edit:
            self.fields['talk'] = forms.ModelChoiceField(
                    Person.objects.get(pk=person).talk_set.all(),
                    label='Talk', empty_label=None)
            return
        if not person:
            self.fields['talk'] = forms.ModelChoiceField(Person.objects.all(),
                    label='Person', empty_label=None)
            self.fields.__delitem__('quote')
            self.fields.__delitem__('notes')
        else:
            self.fields['talk'] = forms.ModelChoiceField(
                    Person.objects.get(pk=person).talk_set.all(),
                    label='Talk', empty_label=None)
            
    topic = forms.CharField(label='Topic',
            widget=forms.TextInput({'readonly':True}))
    talk = forms.CharField(label='Talk', max_length=100,
            widget=forms.TextInput({'readonly':True}))
    edit = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = TalkEntry
        fields = ['topic','talk','quote', 'notes']

class RelatedTopicForm(forms.Form):
    related_topic = forms.ModelChoiceField(Topic.objects.all(), label='Topic',
            empty_label=None)

class ScriptureSet(object):
    def __init__(self):
        self.books = []

class Book(object):
    def __init__(self, name):
        self.name = name
        self.refs = []

    def num_refs(self):
        return len(self.refs)



