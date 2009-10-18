from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django import forms
from studyjournal.topicalguide.models import Topic, Entry, TalkEntry
from studyjournal.topicalguide.models import QuoteEntry, ScriptureReferenceEntry
from studyjournal.talks.models import Person, Talk

def index(request):
    topics = [x for x in Topic.objects.all()]
    topics.sort(key=lambda x: x.index_name())
    return render_to_response('topicalguide/index.html', {'topics' : topics})

def topic(request, topic_name):
    topic = get_object_or_404(Topic, name=topic_name)
    return render_to_response('topicalguide/topic.html', {'topic' : topic})

def add_topic(request):
    if request.POST:
        new_topic = Topic(name=request.POST['name'],
                notes=request.POST['notes'])
        new_topic.save()
        return HttpResponseRedirect('/topics/')
    form = AddTopicForm()
    page_vars = dict()
    page_vars['form'] = form
    page_vars['submit_label'] = "Add topic"
    page_vars['header'] = "Add a new topic"
    return render_to_response('topicalguide/add_form.html', page_vars)

def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.POST:
        topic.name = request.POST['name']
        topic.notes = request.POST['notes']
        topic.save()
        return HttpResponseRedirect('/topic/'+topic.name)
    form = AddTopicForm(instance=topic)
    page_vars = dict()
    page_vars['form'] = form
    page_vars['submit_label'] = "Edit topic"
    page_vars['header'] = "Edit topic " + topic.name
    return render_to_response('topicalguide/add_form.html', page_vars)


def add_scripture_entry(request, topic_name, **kwds):
    if request.POST:
        if request.POST['edit'] != 'False':
            entry = ScriptureReferenceEntry.objects.get(pk=request.POST['edit'])
            entry.notes = request.POST['notes']
            entry.reference = request.POST['reference']
        else:
            entry = ScriptureReferenceEntry(
                    topic=Topic.objects.get(name=topic_name),
                    notes=request.POST['notes'],
                    reference=request.POST['reference'],
                    )
        entry.save()
        return HttpResponseRedirect('/topic/'+topic_name)
    page_vars = dict()
    if kwds.has_key('entry_id'):
        entry = ScriptureReferenceEntry.objects.get(pk=kwds['entry_id'])
        form = AddScriptureForm(initial={'topic': topic_name,
                'notes': entry.notes,
                'reference': entry.reference,
                'edit': entry.id})
        page_vars['submit_label'] = "Edit reference"
        page_vars['header'] = "Edit a scripture reference in " + topic_name
    else:
        form = AddScriptureForm(initial={'topic': topic_name,
                'edit': 'False'})
        page_vars['submit_label'] = "Add reference"
        page_vars['header'] = "Add a scripture reference to " + topic_name
    page_vars['form'] = form
    return render_to_response('topicalguide/add_form.html', page_vars)

def add_talk_entry(request, topic_name, **kwds):
    if request.POST and request.POST['edit'] != 'Person':
        if request.POST['edit'] != 'False':
            entry = TalkEntry.objects.get(pk=request.POST['edit'])
            entry.notes = request.POST['notes']
            entry.quote = request.POST['quote']
        else:
            entry = TalkEntry(
                    topic=Topic.objects.get(name=topic_name),
                    notes=request.POST['notes'],
                    talk=Talk.objects.get(pk=request.POST['talk']),
                    quote=request.POST['quote'],
                    )
        entry.save()
        return HttpResponseRedirect('/topic/'+topic_name)
    page_vars = dict()
    if request.POST:
        form = AddTalkForm(person=request.POST['talk'],
                initial={'topic': topic_name,
                'edit': 'False'})
        page_vars['submit_label'] = "Add Talk"
        page_vars['header'] = "Add a talk to " + topic_name
    elif kwds.has_key('entry_id'):
        entry = TalkEntry.objects.get(pk=kwds['entry_id'])
        form = AddTalkForm(edit=True, initial={'topic': topic_name,
                'talk': entry.talk.__unicode__(),
                'quote': entry.quote,
                'notes': entry.notes,
                'edit': entry.id})
        page_vars['submit_label'] = "Edit talk"
        page_vars['header'] = "Edit a quote for a talk in " + topic_name
    else:
        form = AddTalkForm(initial={'topic': topic_name,
                'edit': 'Person'})
        page_vars['submit_label'] = "Select Talk"
        page_vars['header'] = "Add a talk to " + topic_name
        page_vars['subheader'] = "Pick a person first"
    page_vars['form'] = form
    return render_to_response('topicalguide/add_form.html', page_vars)

class AddTopicForm(forms.ModelForm):
    class Meta:
        model = Topic

class AddScriptureForm(forms.ModelForm):
    topic = forms.CharField(label='Topic',
            widget=forms.TextInput({'readonly':True}))
    edit = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = ScriptureReferenceEntry
        fields = ['topic','reference','notes']

class AddTalkForm(forms.ModelForm):
    def __init__(self, edit=False, person=None, talk=None, *args, **kwds):
        super(AddTalkForm, self).__init__(*args, **kwds)
        if edit or talk:
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

class AddTalkForm1(forms.Form):
    person = forms.ModelChoiceField(Person.objects.all(), label='Person')


