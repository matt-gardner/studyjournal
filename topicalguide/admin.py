#!/usr/bin/env python

from studyjournal.topicalguide.models import Topic, TalkEntry, QuoteEntry, ScriptureReferenceEntry
from django.contrib import admin

class ScriptureReferenceInline(admin.TabularInline):
    model = ScriptureReferenceEntry
    extra = 1

class TalkInline(admin.TabularInline):
    model = TalkEntry
    extra = 1

class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ['name',]
    inlines = [ScriptureReferenceInline]


admin.site.register(Topic, TopicAdmin)

# vim: et sw=4 sts=4
