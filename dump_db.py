#!/usr/bin/env python

from studyjournal.talks.models import Person, Talk
from subprocess import Popen
from month import make_month_str
import os

def main():
    output_people()
    output_talks()

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

if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
