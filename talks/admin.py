#!/usr/bin/env python

from studyjournal.talks.models import Talk, Calling, Person
from django.contrib import admin

class TalkAdmin(admin.ModelAdmin):
    list_display = ('speaker', 'speakername', 'title', 'date')
    list_display_links = ('title',)
    list_filter = ['date', 'speaker']
    search_fields = ['speaker']
    date_hierarchy = 'date'
    ordering = ['speaker', 'speakername', 'date']

class CallingInline(admin.TabularInline):
    model = Calling
    extra = 1

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'callings')
    inlines = [CallingInline]
    ordering = ('name',)

admin.site.register(Talk, TalkAdmin)
admin.site.register(Person, PersonAdmin)

# vim: et sw=4 sts=4
