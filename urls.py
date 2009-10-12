from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'studyjournal.talks.views.index'),
    (r'^person/(?P<person_id>\d+)/$', 'studyjournal.talks.views.person'),
    (r'^talk/(?P<talk_id>\d+)/$', 'studyjournal.talks.views.talk'),
    (r'^topics/$', 'studyjournal.topicalguide.views.index'),
    (r'^topic/(?P<topic_name>.*)/$', 'studyjournal.topicalguide.views.topic'),
    (r'^admin/(.*)', admin.site.root),
)
