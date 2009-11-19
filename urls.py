from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

topicname = '(?P<topic_name>[\'\w,\:\s]+)'

urlpatterns = patterns('',
    (r'^$', 'studyjournal.talks.views.index'),
    (r'^person/(?P<person_id>\d+)/$', 'studyjournal.talks.views.person'),
    (r'^talk/(?P<talk_id>\d+)/$', 'studyjournal.talks.views.talk'),
    (r'^topics/$', 'studyjournal.topicalguide.views.index'),
    (r'^topics/add/$', 'studyjournal.topicalguide.views.add_topic'),
    (r'^topics/edit(?P<topic_id>\d+)/$',
        'studyjournal.topicalguide.views.edit_topic'),
    (r'^topic/'+topicname+'/$',
        'studyjournal.topicalguide.views.topic'),
    (r'^topic/'+topicname+'/addrt$',
            'studyjournal.topicalguide.views.add_related_topic'),
    (r'^topic/'+topicname+'/addsr$',
            'studyjournal.topicalguide.views.add_scripture_entry'),
    (r'^topic/'+topicname+'/sr(?P<entry_id>\d+)/$',
            'studyjournal.topicalguide.views.add_scripture_entry'),
    (r'^topic/'+topicname+'/addq$',
            'studyjournal.topicalguide.views.add_quote'),
    (r'^topic/'+topicname+'/q(?P<entry_id>\d+)/$',
            'studyjournal.topicalguide.views.add_quote'),
    (r'^topic/'+topicname+'/addt$',
            'studyjournal.topicalguide.views.add_talk_entry'),
    (r'^topic/'+topicname+'/t(?P<entry_id>\d+)/$',
            'studyjournal.topicalguide.views.add_talk_entry'),
    (r'^admin/(.*)', admin.site.root),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}),

)
