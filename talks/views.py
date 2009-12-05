from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from studyjournal.talks.models import Talk, Person
from studyjournal.topicalguide.models import Topic, TalkEntry
from datetime import date, datetime
from django import forms

def index(request):
    people_list = Person.objects.all().order_by('lastname')
    return render_to_response('talks/index.html', {'people_list': people_list})

def person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    talks = person.talk_set.all().order_by('-date')
    callings = person.calling_set.all()
    return render_to_response('talks/person.html', 
            {'person': person, 'talks': talks, 'callings': callings})

def talk(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)
    # This is a pretty big hack, but it was the only way I could figure out
    # to get the select box to fit inside the table.
    topicform = AddTalkToTopicForm()._html_output('%(field)s','','','',False)
    return render_to_response('talks/talk.html',
            {'talk': talk, 'topicform': topicform})

def add_talk_to_topic(request, talk_id):
    if 'topic' in request.POST:
        topic = get_object_or_404(Topic, pk=request.POST['topic'])
        talk = get_object_or_404(Talk, pk=talk_id)
        entry = TalkEntry(topic=topic, talk=talk)
        entry.save()
        topic.last_modified = datetime.now()
        topic.save()
    return HttpResponseRedirect('/talk/'+talk_id)

def callings(request):
    callings = Callings()
    if 'year' in request.GET:
        year = int(request.GET['year'])
    else:
        year = date.today().year
    if 'month' in request.GET:
        month = int(request.GET['month'])
    else:
        month = date.today().month
    if 'day' in request.GET:
        day = int(request.GET['day'])
    else:
        day = date.today().day
    for person in Person.objects.all():
        try:
            calling = person.get_calling(date(year, month, day))
        except ValueError:
            continue
        if calling == 'P':
            callings.president = person
        if calling == 'FC':
            callings.first_counselor = person
        if calling == 'SC':
            callings.second_counselor = person
        if calling == 'A':
            callings.apostles.append(person)
        if calling == 'S':
            callings.seventy.append(person)
    return render_to_response('talks/callings.html',
            {'callings': callings, 'year': year, 'month': month, 'day': day})


class Callings(object):
    def __init__(self):
        self.president = None
        self.first_counselor = None
        self.second_counselor = None
        self.apostles = []
        self.seventy = []


class AddTalkToTopicForm(forms.Form):
    topic = forms.ModelChoiceField(Topic.objects.all(), label="",
            empty_label=None)

