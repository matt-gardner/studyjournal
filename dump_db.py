#!/usr/bin/env python

import os, sys

sys.path.append(os.curdir+'/../')
os.environ['DJANGO_SETTINGS_MODULE'] = 'studyjournal.settings'

import simplejson

from dirutil import create_dirs_and_open
from month import make_month_str
from optparse import OptionParser
from studyjournal.talks.models import Person, Talk
from studyjournal.topicalguide.models import Topic, TalkEntry, Quote, Reference

BASE_DIR = ''

def main():
    parser = OptionParser()
    parser.add_option('', '--talks',
            dest='talks',
            default=False,
            action='store_true',
            help='Dump talks'
            )
    parser.add_option('', '--people',
            dest='people',
            default=False,
            action='store_true',
            help='Dump people'
            )
    parser.add_option('', '--topics',
            dest='topics',
            default=False,
            action='store_true',
            help='Dump topics'
            )
    parser.add_option('-b', '--base-dir',
            dest='base_dir',
            default='data',
            help='Base directory for the data dump'
            )
    options, args = parser.parse_args()
    if os.path.exists(options.base_dir):
        print 'The dump directory you gave already exists!  Data could be '\
                'overwritten.\nQuitting...'
        exit(-1)
    global BASE_DIR
    BASE_DIR = options.base_dir
    if not BASE_DIR.endswith('/'):
        BASE_DIR += '/'
    did_something = False
    if options.people:
        did_something = True
        output_people()
    if options.talks:
        did_something = True
        output_talks()
    if options.topics:
        did_something = True
        output_topics()
    if not did_something:
        print 'Did you forget to specify what you wanted to output?'

def output_people():
    f = open(BASE_DIR + 'people.txt', 'w')
    for person in Person.objects.all().order_by('lastname'):
        if person.lastname == 'Other':
            continue
        namegender = person.name()+': '+person.gender+'\n'
        f.write(namegender.encode('utf-8'))
        if person.wikipedia_bio:
            f.write('  Wikipedia: '+person.wikipedia_bio+'\n')
        if person.ga_bio:
            f.write('  GA Bio: '+person.ga_bio+'\n')
        for calling in person.calling_set.all():
            callingstr = calling.__unicode__()+': '
            callingstr += str(calling.startdate.day)+'/'+\
                    str(calling.startdate.month)+'/'+\
                    str(calling.startdate.year)+'-'
            if calling.enddate:
                callingstr += str(calling.enddate.day)+'/'+\
                        str(calling.enddate.month)+'/'+\
                        str(calling.enddate.year)
            else:
                callingstr += 'present'
            f.write('  '+callingstr+'\n')
    f.close()

def output_talks():
    talks = []
    for talk in Talk.objects.all():
        typestr = talk.type.lower()
        yearstr = str(talk.date.year)
        monthstr = make_month_str(talk.date.month)
        talkfile = typestr+'/'+yearstr+'/'+monthstr+'/'+str(talk.id)+'.txt'
        talks.append(talkfile)
        output_talk(talk, talkfile)
    f = open(BASE_DIR + 'indexfile.txt', 'w')
    for talk in talks:
        f.write(talk+'\n')
    f.close()

def output_talk(talk, talkfile):
    f = create_dirs_and_open(BASE_DIR + talkfile)
    json = {}
    if talk.speakername:
        json['speaker'] = talk.speakername
    else:
        json['speaker'] = talk.speaker.name()
    try:
        calling = talk.speaker.get_calling(talk.date)
        json['calling'] = calling
    except ValueError:
        json['calling'] = 'Unknown'
    json['gender'] = talk.speaker.gender
    json['title'] = talk.title
    json['topic'] = talk.topic
    json['type'] = talk.type
    json['year'] = talk.date.year
    json['month'] = talk.date.month
    json['day'] = talk.date.day
    json['link'] = talk.externallink
    json['text'] = talk.text
    f.write(simplejson.dumps(json, indent=2))
    f.close()

def output_topics():
    f = open(BASE_DIR + 'topics.txt', 'w')
    for topic in Topic.objects.all().order_by('name'):
        f.write('Topic: ' + topic.name + '\n')
        f.write('Subheading: ' + topic.subheading + '\n')
        f.write('Index name: ' + topic.indexname + '\n')
        last_modified_string = str(topic.last_modified.year) + ', '
        last_modified_string += str(topic.last_modified.month) + ', '
        last_modified_string += str(topic.last_modified.day) + ', '
        last_modified_string += str(topic.last_modified.hour) + ', '
        last_modified_string += str(topic.last_modified.minute) + ', '
        last_modified_string += str(topic.last_modified.second)
        f.write('Last Modified: ' + last_modified_string + '\n')
        f.write('Notes: ' + topic.notes + '\n')
        f.write('Entries: \n')
        for sr_entry in topic.reference_set.all():
            f.write('Scripture: ' + sr_entry.reference + '\n')
            f.write('Notes: ' + sr_entry.notes.encode('utf-8') + '\n')
        for q_entry in topic.quote_set.all():
            f.write('Quote: ' + q_entry.quote.encode('utf-8') + '\n')
            f.write('Person: ' + q_entry.person.name().encode('utf-8') + '\n')
            f.write('Source: ' + q_entry.source.encode('utf-8') + '\n')
            f.write('Notes: ' + q_entry.notes.encode('utf-8') + '\n')
        for t_entry in topic.talkentry_set.all():
            f.write('Talk: ' + t_entry.talk.title.encode('utf-8') + '\n')
            f.write('Speaker: ' +
                    t_entry.talk.speaker.name().encode('utf-8') + '\n')
            f.write('Quote: ' + t_entry.quote.encode('utf-8') + '\n')
            f.write('Notes: ' + t_entry.notes.encode('utf-8') + '\n')
        f.write('\n')

    f.write('Related Topics: \n')
    for topic in Topic.objects.all().order_by('name'):
        for t in topic.related_topics.all():
            f.write(topic.name + ' === ' + t.name + '\n')
    f.write('\n')
    f.close()


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
