from django.shortcuts import render_to_response, get_object_or_404
from studyjournal.talks.models import Talk, Person

def index(request):
    people_list = Person.objects.all().order_by('lastname')
    return render_to_response('talks/index.html', {'people_list': people_list})

def person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    talks = Talk.objects.filter(speaker=person_id)
    callings = person.calling_set.all()
    return render_to_response('talks/person.html', 
            {'person': person, 'talks': talks, 'callings': callings})

def talk(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)
    return render_to_response('talks/talk.html', {'talk': talk})


