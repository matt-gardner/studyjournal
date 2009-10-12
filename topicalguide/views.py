from django.shortcuts import render_to_response, get_object_or_404
from studyjournal.topicalguide.models import Topic, Entry, TalkEntry, QuoteEntry, ScriptureReferenceEntry

def index(request):
    topics = Topic.objects.all()
    return render_to_response('topicalguide/index.html', {'topics' : topics})

def topic(request, topic_name):
    topic = get_object_or_404(Topic, name=topic_name)
    return render_to_response('topicalguide/topic.html', {'topic' : topic})


