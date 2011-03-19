from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

entry_id = '(?P<entry_id>\d+)'
person_id = '(?P<person_id>\d+)'
rating_id = '(?P<rating_id>\d+)'
talk_id = '(?P<talk_id>\d+)'
topic_id = '(?P<topic_id>\d+)'
width = '(?P<width>[^/]+)'

urlpatterns = patterns('',
    (r'^$',
        'studyjournal.talks.views.index'),

    (r'^people/$',
        'studyjournal.talks.views.people'),
    (r'^person/'+person_id+'/$',
        'studyjournal.talks.views.person'),
    (r'^person/'+person_id+'/edit$',
        'studyjournal.talks.views.edit_person'),
    (r'^person/'+person_id+'/addtalk$',
        'studyjournal.talks.views.add_talk'),

    (r'^talk/'+talk_id+'/$',
        'studyjournal.talks.views.talk'),
    (r'^talk/'+talk_id+'/edit$',
        'studyjournal.talks.views.edit_talk'),
    (r'^talk/'+talk_id+'/addrating$',
        'studyjournal.talks.views.add_rating_to_talk'),
    (r'^talk/'+talk_id+'/rating'+rating_id+'/$',
        'studyjournal.talks.views.add_rating_to_talk'),
    (r'^talk/'+talk_id+'/addtotopic$',
        'studyjournal.talks.views.add_talk_to_topic'),

    (r'^talk-pdf/'+talk_id+'/'+width+'/$',
        'studyjournal.talks.views.talk_pdf'),

    (r'^topics/$',
        'studyjournal.topicalguide.views.index'),
    (r'^topics/add/$',
        'studyjournal.topicalguide.views.add_topic'),
    (r'^topics/edit'+topic_id+'/$',
        'studyjournal.topicalguide.views.edit_topic'),
    (r'^topic/'+topic_id+'/$',
        'studyjournal.topicalguide.views.topic'),
    (r'^topic/'+topic_id+'/addrt$',
        'studyjournal.topicalguide.views.add_related_topic'),
    (r'^topic/'+topic_id+'/addsr$',
        'studyjournal.topicalguide.views.add_scripture_entry'),
    (r'^topic/'+topic_id+'/sr'+entry_id+'/$',
        'studyjournal.topicalguide.views.add_scripture_entry'),
    (r'^topic/'+topic_id+'/addq$',
        'studyjournal.topicalguide.views.add_quote'),
    (r'^topic/'+topic_id+'/q'+entry_id+'/$',
        'studyjournal.topicalguide.views.add_quote'),
    (r'^topic/'+topic_id+'/addt$',
        'studyjournal.topicalguide.views.add_talk_entry'),
    (r'^topic/'+topic_id+'/t'+entry_id+'/$',
        'studyjournal.topicalguide.views.add_talk_entry'),

    (r'^scriptures/$',
        'studyjournal.topicalguide.views.scriptures'),

    (r'^callings/$',
        'studyjournal.talks.views.callings'),

    (r'^admin/(.*)',
        admin.site.root),

    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),

)
