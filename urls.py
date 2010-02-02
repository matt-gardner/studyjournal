from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

topicname = '(?P<topic_id>\d+)'

urlpatterns = patterns('',
    (r'^$', 'studyjournal.talks.views.index'),
    (r'^people/$', 'studyjournal.talks.views.people'),
    (r'^person/(?P<person_id>\d+)/$', 'studyjournal.talks.views.person'),
    (r'^person/(?P<person_id>\d+)/edit$', 'studyjournal.talks.views.edit_person'),
    (r'^person/(?P<person_id>\d+)/addtalk$', 'studyjournal.talks.views.add_talk'),
    (r'^talk/(?P<talk_id>\d+)/$', 'studyjournal.talks.views.talk'),
    (r'^talk/(?P<talk_id>\d+)/edit$', 'studyjournal.talks.views.edit_talk'),
    (r'^talk/(?P<talk_id>\d+)/addtotopic$',
            'studyjournal.talks.views.add_talk_to_topic'),
    (r'^topics/$', 'studyjournal.topicalguide.views.index'),
    (r'^topics/add/$', 'studyjournal.topicalguide.views.add_topic'),
    (r'^topics/edit(?P<topic_id>\d+)/$',
            'studyjournal.topicalguide.views.edit_topic'),
    (r'^topic/(?P<topic_id>\d+)/$',
            'studyjournal.topicalguide.views.topic'),
    (r'^topic/(?P<topic_id>\d+)/addrt$',
            'studyjournal.topicalguide.views.add_related_topic'),
    (r'^topic/(?P<topic_id>\d+)/addsr$',
            'studyjournal.topicalguide.views.add_scripture_entry'),
    (r'^topic/(?P<topic_id>\d+)/sr(?P<entry_id>\d+)/$',
            'studyjournal.topicalguide.views.add_scripture_entry'),
    (r'^topic/(?P<topic_id>\d+)/addq$',
            'studyjournal.topicalguide.views.add_quote'),
    (r'^topic/(?P<topic_id>\d+)/q(?P<entry_id>\d+)/$',
            'studyjournal.topicalguide.views.add_quote'),
    (r'^topic/(?P<topic_id>\d+)/addt$',
            'studyjournal.topicalguide.views.add_talk_entry'),
    (r'^topic/(?P<topic_id>\d+)/t(?P<entry_id>\d+)/$',
            'studyjournal.topicalguide.views.add_talk_entry'),
    (r'^scriptures/$', 'studyjournal.topicalguide.views.scriptures'),
    (r'^callings/$', 'studyjournal.talks.views.callings'),
    (r'^admin/(.*)', admin.site.root),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),

)
