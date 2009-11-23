#!/usr/bin/env python

from studyjournal.talks.models import Person, Talk
from studyjournal.topicalguide.models import Topic, TalkEntry, QuoteEntry
from studyjournal.topicalguide.models import ScriptureReferenceEntry
from subprocess import Popen
from month import make_month_str
from optparse import OptionParser
import os

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
    options, args = parser.parse_args()
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
    f = open('people.txt', 'w')
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
    for type, long_type in Talk.TYPE_CHOICES:
        if not os.path.exists(type.lower()):
            proc = Popen(('mkdir', type.lower()))
            proc.wait()
    for talk in Talk.objects.all():
        typestr = talk.type.lower()
        yearstr = str(talk.date.year)
        monthstr = make_month_str(talk.date.month)
        if not os.path.exists(typestr+'/'+yearstr):
            proc = Popen(('mkdir', typestr+'/'+yearstr))
            proc.wait()
        if not os.path.exists(typestr+'/'+yearstr+'/'+monthstr):
            proc = Popen(('mkdir', typestr+'/'+yearstr+'/'+monthstr))
            proc.wait()
        talkfile = typestr+'/'+yearstr+'/'+monthstr+'/'+str(talk.id)+'.txt'
        talks.append(talkfile)
        output_talk(talk, talkfile)
    f = open('indexfile.txt', 'w')
    for talk in talks:
        f.write(talk+'\n')
    f.close()

def output_talk(talk, talkfile):
        f = open(talkfile, 'w')
        if talk.speakername:
            f.write('SPEAKER: '+talk.speakername.encode('utf-8')+'\n')
        else:
            f.write('SPEAKER: '+talk.speaker.name().encode('utf-8')+'\n')
        try:
            calling = talk.speaker.get_calling(talk.date)
            f.write('CALLING: '+calling.encode('utf-8')+'\n')
        except ValueError:
            f.write('CALLING: Unknown\n')
        f.write('GENDER: '+talk.speaker.gender.encode('utf-8')+'\n')
        f.write('TITLE: '+talk.title.encode('utf-8')+'\n')
        f.write('TOPIC: '+talk.topic.encode('utf-8')+'\n')
        f.write('TYPE: '+talk.type.encode('utf-8')+'\n')
        f.write('YEAR: '+str(talk.date.year)+'\n')
        f.write('MONTH: '+str(talk.date.month)+'\n')
        f.write('DAY: '+str(talk.date.day)+'\n')
        f.write('LINK: '+str(talk.externallink)+'\n')
        f.write('\n')
        f.write(talk.text.encode('utf-8'))
        f.close()

def output_topics():
    f = open('topics.txt', 'w')
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
        for sr_entry in topic.scripturereferenceentry_set.all():
            f.write('Scripture: ' + sr_entry.reference + '\n')
            f.write('Notes: ' + sr_entry.notes + '\n')
        for q_entry in topic.quoteentry_set.all():
            f.write('Quote: ' + q_entry.quote.encode('utf-8') + '\n')
            f.write('Person: ' + q_entry.person.name().encode('utf-8') + '\n')
            f.write('Source: ' + q_entry.source.encode('utf-8') + '\n')
            f.write('Notes: ' + q_entry.notes + '\n')
        for t_entry in topic.talkentry_set.all():
            f.write('Talk: ' + t_entry.talk.title.encode('utf-8') + '\n')
            f.write('Speaker: ' +
                    t_entry.talk.speaker.name().encode('utf-8') + '\n')
            f.write('Quote: ' + t_entry.quote.encode('utf-8') + '\n')
            f.write('Notes: ' + t_entry.notes + '\n')
        f.write('\n')
    f.close()
    

if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
