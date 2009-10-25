from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'studyjournal.talks.views.index'),
    (r'^person/(?P<person_id>\d+)/$', 'studyjournal.talks.views.person'),
    (r'^talk/(?P<talk_id>\d+)/$', 'studyjournal.talks.views.talk'),
    (r'^topics/$', 'studyjournal.topicalguide.views.index'),
    (r'^topics/add/$', 'studyjournal.topicalguide.views.add_topic'),
    (r'^topics/edit(?P<topic_id>\d+)/$', 'studyjournal.topicalguide.views.edit_topic'),
    (r'^topic/(?P<topic_name>[\w,\:\s]+)/$',
        'studyjournal.topicalguide.views.topic'),
    (r'^topic/(?P<topic_name>[\w,\:\s]+)/addsr$',
            'studyjournal.topicalguide.views.add_scripture_entry'),
    (r'^topic/(?P<topic_name>[\w,\:\s]+)/sr(?P<entry_id>\d+)/$',
            'studyjournal.topicalguide.views.add_scripture_entry'),
    (r'^topic/(?P<topic_name>[\w,\:\s]+)/addq$',
            'studyjournal.topicalguide.views.add_quote'),
    (r'^topic/(?P<topic_name>[\w,\:\s]+)/q(?P<entry_id>\d+)/$',
            'studyjournal.topicalguide.views.add_quote'),
    (r'^topic/(?P<topic_name>[\w,\:\s]+)/addt$',
            'studyjournal.topicalguide.views.add_talk_entry'),
    (r'^topic/(?P<topic_name>[\w,\:\s]+)/t(?P<entry_id>\d+)/$',
            'studyjournal.topicalguide.views.add_talk_entry'),
    (r'^admin/(.*)', admin.site.root),
)
