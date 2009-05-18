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
    if not os.path.exists('gc'):
        proc = Popen(('mkdir','gc'))
        proc.wait()
    for talk in Talk.objects.filter(type='GC'):
        yearstr = str(talk.date.year)
        monthstr = make_month_str(talk.date.month)
        if not os.path.exists('gc/'+yearstr):
            proc = Popen(('mkdir', 'gc/'+yearstr))
            proc.wait()
        if not os.path.exists('gc/'+yearstr+'/'+monthstr):
            proc = Popen(('mkdir', 'gc/'+yearstr+'/'+monthstr))
            proc.wait()
        talkfile = 'gc/'+yearstr+'/'+monthstr+'/'+str(talk.id)+'.txt'
        talks.append(talkfile)
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
    f = open('indexfile.txt', 'w')
    for talk in talks:
        f.write(talk+'\n')
    f.close()

if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
