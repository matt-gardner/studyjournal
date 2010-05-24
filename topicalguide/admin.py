#!/usr/bin/env python

from studyjournal.topicalguide.models import Topic, TalkEntry, Quote, Reference
from django.contrib import admin

class ReferenceInline(admin.TabularInline):
    model = Reference
    extra = 1

class TalkInline(admin.TabularInline):
    model = TalkEntry
    extra = 1

class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ['name',]
    inlines = [ReferenceInline]


admin.site.register(Topic, TopicAdmin)

# vim: et sw=4 sts=4
