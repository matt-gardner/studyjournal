from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from studyjournal.talks.models import Talk, Person, Calling, Rating
from studyjournal.topicalguide.models import Topic, TalkEntry
from datetime import date, datetime
from django import forms


# Basic views
#############

def index(request):
    return render_to_response('index.html')


def people(request):
    people = Person.objects.all().order_by('lastname')
    people_list = PeopleList()
    for person in people:
        letter = person.lastname[0]
        if letter not in people_list.first_letters():
            people_list.letters.append(Letter(letter))
        people_list.get_letter(letter).people.append(person)
    return render_to_response('talks/people.html', {'people_list': people_list})


def person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    talks = person.talk_set.all().order_by('-date')
    callings = person.calling_set.all()
    return render_to_response('talks/person.html', 
            {'person': person, 'talks': talks, 'callings': callings})


def talk(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)
    if 'delete' in request.GET:
        delete = request.GET['delete']
        if 'rating' in delete:
            rating = Rating.objects.get(pk=delete[6:])
            rating.delete()
        return HttpResponseRedirect('/talk/'+talk_id)
    # This is a pretty big hack, but it was the only way I could figure out
    # to get the select box to fit inside the table.
    topicform = AddTalkToTopicForm()._html_output('%(field)s','','','',False)
    page_vars = dict()
    page_vars['talk'] = talk
    page_vars['topicform'] = topicform
    page_vars['ratings'] = talk.rating_set.order_by('-rating')
    page_vars['link'] = talk.externallink
    return render_to_response('talks/talk.html', page_vars)


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
    d = date(year, month, day)
    for person in Person.objects.all():
        try:
            calling = person.get_calling(d)
        except ValueError:
            continue
        if calling == 'P':
            callings.president = person
        if calling == 'FC':
            callings.first_counselor = person
        if calling == 'SC':
            callings.second_counselor = person
        if calling == 'C':
            callings.extra_counselors.append(person)
        if calling == 'A':
            callings.apostles.append(person)
        if calling == 'S':
            callings.seventy.append(person)
        if calling == 'B':
            callings.presiding_bishop = person
        if calling == 'PB':
            callings.presiding_bishopric.append(person)
    callings.sort_by_date()
    return render_to_response('talks/callings.html',
            {'callings': callings, 'year': year, 'month': month, 'day': day})


# Adding and editing views
##########################

def edit_person(request, person_id):
    CallingFormSet = forms.models.inlineformset_factory(Person, Calling,
            extra=1)
    person = get_object_or_404(Person, pk=person_id)
    if request.POST:
        form = EditPersonForm(request.POST, instance=person)
        callingformset = CallingFormSet(request.POST, instance=person)
        if callingformset.is_valid():
            callingformset.save()
        form.save()
        return HttpResponseRedirect('/person/'+person_id)
    page_vars = dict()
    form = EditPersonForm(instance=person)
    callingformset = CallingFormSet(instance=person)
    page_vars['form'] = form.as_table() + callingformset.as_table()
    page_vars['submit_label'] = 'Edit person'
    page_vars['header'] = 'Edit '+person.name()
    return render_to_response('add_form.html', page_vars)


def edit_talk(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)
    if request.POST:
        form = EditTalkForm(None, request.POST, instance=talk)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/talk/'+talk_id)
    page_vars = dict()
    form = EditTalkForm(instance=talk)
    page_vars['form'] = form
    page_vars['submit_label'] = 'Edit Talk'
    page_vars['header'] = 'Edit '+talk.__unicode__()
    return render_to_response('add_form.html', page_vars)


def add_talk(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    if request.POST:
        talk = Talk(speaker=person)
        talk.date = request.POST['date']
        talk.title = request.POST['title']
        talk.text = request.POST['text']
        talk.topic = request.POST['topic']
        talk.type = request.POST['type']
        talk.externallink = request.POST['externallink']
        talk.audiofile = request.POST['audiofile']
        talk.audiolink = request.POST['audiolink']
        talk.save()
        return HttpResponseRedirect('/person/'+person_id)
    form = EditTalkForm(person=person, initial={'speaker':person.name()})
    page_vars = dict()
    page_vars['form'] = form
    page_vars['submit_label'] = 'Add Talk'
    page_vars['header'] = 'Add talk to '+person.name()
    return render_to_response('add_form.html', page_vars)


def add_talk_to_topic(request, talk_id):
    if 'topic' in request.POST:
        topic = get_object_or_404(Topic, pk=request.POST['topic'])
        talk = get_object_or_404(Talk, pk=talk_id)
        entry = TalkEntry(topic=topic, talk=talk)
        entry.save()
        topic.last_modified = datetime.now()
        topic.save()
    return HttpResponseRedirect('/talk/'+talk_id)


def add_rating_to_talk(request, talk_id, rating_id=None):
    talk = Talk.objects.get(pk=talk_id)
    if request.POST:
        if request.POST['edit'] != 'False':
            rating = Rating.objects.get(pk=request.POST['edit'])
            rating.user = User.objects.get(pk=request.POST['user'])
            rating.rating = request.POST['rating']
            rating.comment = request.POST['comment']
        else:
            rating = Rating(
                    talk=talk,
                    user=User.objects.get(pk=request.POST['user']),
                    rating=request.POST['rating'],
                    comment=request.POST['comment'].strip(),
                    )
        rating.save()
        return HttpResponseRedirect('/talk/'+talk_id)
    page_vars = dict()
    if rating_id:
        rating = Rating.objects.get(pk=rating_id)
        form = AddRatingToTalkForm(instance=rating)
        form.fields['edit'].initial = rating_id
        page_vars['submit_label'] = 'Edit rating'
        page_vars['header'] = 'Editing rating for ' + talk.__unicode__()
    else:
        form = AddRatingToTalkForm(initial={'edit': 'False'})
        page_vars['submit_label'] = 'Add rating'
        page_vars['header'] = 'Add rating for ' + talk.__unicode__()
    page_vars['form'] = form
    return render_to_response('add_form.html', page_vars)


# Other views
#############

def talk_pdf(request, talk_id, width):
    from speed_reading import format_text
    width = float(width)
    text = Talk.objects.get(pk=talk_id).text
    pdf_loc = format_text.make_pdf(text, width, '/tmp/')
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'filename=%s' % pdf_loc
    response.write(open(pdf_loc).read())
    return response


# Classes for forms and other stuff
###################################

class Callings(object):
    def __init__(self):
        self.president = None
        self.first_counselor = None
        self.second_counselor = None
        self.extra_counselors = []
        self.apostles = []
        self.seventy = []
        self.presiding_bishop = None
        self.presiding_bishopric = []

    def sort_by_date(self):
        self.apostles.sort(key=lambda x:
                x.calling_set.get(calling='A').startdate)


class AddTalkToTopicForm(forms.Form):
    topic = forms.ModelChoiceField(Topic.objects.all(), label="",
            empty_label=None)


class AddRatingToTalkForm(forms.ModelForm):
    edit = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = Rating
        exclude = ['talk']


class EditPersonForm(forms.ModelForm):
    class Meta:
        model = Person


class EditTalkForm(forms.ModelForm):
    date = forms.DateField(label='Date given (yyyy-mm-dd)')

    def __init__(self, person=None, *args, **kwds):
        super(EditTalkForm, self).__init__(*args, **kwds)
        if person:
            self.fields['speaker'] = forms.CharField(label='Speaker',
                    widget=forms.TextInput({'readonly':True}))
            if person.firstname == 'Other' and person.lastname == 'Other':
                self.fields['speaker'].widget=forms.HiddenInput()
            else:
                self.fields.__delitem__('speakername')
        else:
            self.fields['speakername'].label = 'Speakername (only for Other)'

    class Meta:
        model = Talk


class PeopleList(object):
    def __init__(self):
        self.letters = []

    def first_letters(self):
        return [x.letter for x in self.letters]

    def get_letter(self, l):
        for letter in self.letters:
            if letter.letter == l:
                return letter


class Letter(object):
    def __init__(self, letter):
        self.letter = letter
        self.people = []


# vim: et sw=4 sts=4
