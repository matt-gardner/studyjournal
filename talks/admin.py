#!/usr/bin/env python

from studyjournal.talks.models import Talk
from django.contrib import admin

class TalkAdmin(admin.ModelAdmin):
    list_display = ('speaker', 'title', 'date')
    list_filter = ['date', 'speaker']
    search_fields = ['speaker']
    date_hierarchy = 'date'

admin.site.register(Talk, TalkAdmin)

# vim: et sw=4 sts=4
