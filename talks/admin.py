#!/usr/bin/env python

from studyjournal.talks.models import Talk, Calling, Person
from django.contrib import admin

class TalkAdmin(admin.ModelAdmin):
    list_display = ('speaker', 'speakername', 'title', 'date')
    list_display_links = ('title',)
    list_filter = ['speaker']
    search_fields = ['^speaker__firstname', '^speaker__middlename',
            '^speaker__lastname', '^speaker__suffix', 'speakername', 'title']
    date_hierarchy = 'date'
    ordering = ['speaker', 'speakername', 'date']

class CallingInline(admin.TabularInline):
    model = Calling
    extra = 1

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'firstname', 'middlename', 'lastname', 'suffix',
            'gender', 'numtalks', 'callings', 'ga_bio')
    list_editable = ('firstname', 'middlename', 'lastname', 'suffix', 'gender')
    inlines = [CallingInline]
    ordering = ('lastname',)

admin.site.register(Talk, TalkAdmin)
admin.site.register(Person, PersonAdmin)

# vim: et sw=4 sts=4
