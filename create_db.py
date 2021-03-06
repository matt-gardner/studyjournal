#!/usr/bin/env python

from studyjournal.talks.models import Talk, Person, Calling
from studyjournal.topicalguide.models import Topic, TalkEntry, Quote, Reference
from django.contrib.auth.models import User
from datetime import date, datetime
from name import split_name
from optparse import OptionParser

def main():
    parser = OptionParser()
    parser.add_option('', '--talks',
            dest='talks',
            default=False,
            action='store_true',
            help='Import talks'
            )
    parser.add_option('', '--people',
            dest='people',
            default=False,
            action='store_true',
            help='Import people'
            )
    parser.add_option('', '--topics',
            dest='topics',
            default=False,
            action='store_true',
            help='Import topics'
            )
    parser.add_option('', '--all',
            dest='all',
            default=False,
            action='store_true',
            help='Import everything'
            )
    options, args = parser.parse_args()
    did_something = False
    if options.people or options.all:
        did_something = True
        create_people()
    if options.talks or options.all:
        did_something = True
        create_talks()
    if options.topics or options.all:
        did_something = True
        create_topics()
    if not did_something:
        print 'Did you forget to specify what you wanted to import?'

def create_people():
    peoplefile = open('data/people.txt')
    person = None
    while True:
        line = peoplefile.readline()
        if not line:
            break
        line = line[:-1]
        if line[0] == ' ':
            if 'Wikipedia' in line:
                wiki = line.split(': ')[1]
                person.wikipedia_bio = wiki
                person.save()
                continue
            if 'GA Bio' in line:
                ga_bio = line.split(': ')[1]
                person.ga_bio = ga_bio
                person.save()
                continue
            fields = line.split(': ')
            callingname = fields[0].strip()
            other = None
            for calling in Calling.CALLING_CHOICES:
                if callingname == calling[1]:
                    callingname = calling[0]
                    break
            else:
                other = callingname
                callingname = 'O'
            dates = fields[1].split('-')
            sday, smonth, syear = dates[0].split('/')
            sdate = date(int(syear), int(smonth), int(sday))
            if dates[1] == 'present':
                edate = None
            else:
                eday, emonth, eyear = dates[1].split('/')
                edate = date(int(eyear), int(emonth), int(eday))
            if edate:
                person.calling_set.create(calling=callingname, othername=other,
                        startdate=sdate, enddate=edate)
            else:
                person.calling_set.create(calling=callingname, othername=other,
                        startdate=sdate)
        else:
            name, gender = line.split(': ')
            firstname, middlename, lastname, suffix = split_name(name)
            person = Person(firstname=firstname, middlename=middlename, 
                    lastname=lastname, suffix=suffix, gender=gender)
            person.save()
    person = Person(firstname='Other', lastname='Other', gender='M')
    person.save()


def create_talks():
    indexfile = 'data/indexfile.txt'
    basedir = 'data/'
    f = open(indexfile)
    for file in f:
        talkfile = open(basedir+file[:-1])
        try:
            parse_file(talkfile)
        except (TypeError, ValueError), e:
            print 'Error in parsing talk',file[:-1]
            print str(e)
            continue


def parse_file(talkfile):
    speaker = False
    calling = False
    gender = False
    title = False
    topic = False
    type = False
    year = False
    month = False
    day = False
    link = ''
    audiofile = ''
    audiolink = ''
    while True:
        line = talkfile.readline().decode('utf-8')
        if 'SPEAKER' in line:
            speaker = line[9:-1]
        if 'CALLING' in line:
            calling = line[9:-1]
        if 'GENDER' in line:
            gender = line[8]
        if 'TITLE' in line:
            title = line[7:-1]
        if 'TOPIC' in line:
            topic = line[7:-1]
        if 'TYPE' in line:
            type = line[6:-1]
        if 'YEAR' in line:
            year = line[6:-1]
        if 'MONTH' in line:
            month = line[7:-1]
        if 'DAY' in line:
            day = line[5:-1]
        if 'LINK' in line:
            link = line[6:-1]
        if 'AUDIOFILE' in line:
            audiofile = line[11:-1]
        if 'AUDIOLINK' in line:
            audiolink = line[11:-1]
        if line.isspace():
            break
        if not line:
            break
    text = ''
    for line in talkfile:
        text = text + line.decode('utf-8')
    day = int(day)
    year = int(year)
    month = int(month)
    d = date(year, month, day)
    firstname, middlename, lastname, suffix = split_name(speaker)
    try:
        sid = Person.objects.get(firstname=firstname, middlename=middlename,
                lastname=lastname, suffix=suffix)
        talk = Talk(speaker=sid, date=d, title=title, text=text, topic=topic, 
                type=type, externallink=link, audiofile=audiofile,
                audiolink=audiolink)
    except Person.DoesNotExist:
        sid = Person.objects.get(firstname='Other')
        talk = Talk(speaker=sid, speakername=speaker, date=d, title=title, 
                text=text, topic=topic, type=type, externallink=link,
                audiofile=audiofile, audiolink=audiolink)
    talk.save()


def create_topics():
    f = open('data/topics.txt')
    lines = f.readlines()
    i = 0
    while i < len(lines):
        if lines[i] == '\n':
            i += 1
            continue
        if lines[i][:7] == 'Topic: ':
            name = lines[i][7:-1]
            i += 1
            subheading = lines[i][12:-1]
            i += 1
            indexname = lines[i][12:-1]
            i += 1
            date_str = lines[i][15:-1]
            fields = date_str.split(', ')
            year = int(fields[0])
            month = int(fields[1])
            day = int(fields[2])
            hour = int(fields[3])
            minute = int(fields[4])
            second = int(fields[5])
            dt = datetime(year, month, day, hour, minute, second)
            i += 1
            notes = ''
            while lines[i][:9] != 'Entries: ':
                if lines[i][:7] == 'Notes: ':
                    lines[i] = lines[i][7:]
                notes += lines[i]
                i += 1
            ####################################
            # ONE TIME HACK - PUT THIS IN THE DATAFILE AND REMOVE THESE LINES!!
            ####################################
            username = 'matt'
            if 'Sabrina' in indexname:
                username = 'sabrina'
            ####################################
            user = User.objects.get(username=username)
            topic = Topic(name=name, subheading=subheading, last_modified=dt,
                    indexname=indexname, notes=notes[:-1], user=user)
            topic.save()
            continue
        if lines[i][:9] == 'Entries: ':
            i += 1
            while lines[i] != '\n':
                if lines[i][:11] == 'Scripture: ':
                    i = get_sr_entry(lines, i, topic)
                if lines[i][:6] == 'Talk: ':
                    i = get_t_entry(lines, i, topic)
                if lines[i][:7] == 'Quote: ':
                    i = get_q_entry(lines, i, topic)
        if lines[i][:16] == 'Related Topics: ':
            i += 1
            while lines[i] != '\n':
                t1, t2 = lines[i][:-1].split(' === ')
                t1 = Topic.objects.get(name=t1)
                t2 = Topic.objects.get(name=t2)
                t1.related_topics.add(t2)
                i += 1
        i += 1


def get_sr_entry(lines, i, topic):
    ref = lines[i][11:-1]
    i += 1
    notes = ''
    while (lines[i][:11] != 'Scripture: ' and
            lines[i][:6] != 'Talk: ' and
            lines[i][:7] != 'Quote: ' and
            lines[i] != '\n'):
        if lines[i][:7] == 'Notes: ':
            lines[i] = lines[i][7:]
        notes += lines[i]
        i += 1
    entry = Reference(topic=topic, reference=ref,
            notes=notes[:-1])
    entry.save()
    return i


def get_t_entry(lines, i, topic):
    title = lines[i][6:-1]
    i += 1
    speaker = lines[i][9:-1]
    firstname, middlename, lastname, suffix = split_name(speaker)
    sid = Person.objects.get(firstname=firstname, middlename=middlename,
            lastname=lastname, suffix=suffix)
    talk = Talk.objects.get(speaker=sid, title=title)
    i += 1
    quote = ''
    while (lines[i][:7] != 'Notes: '):
        if lines[i][:7] == 'Quote: ':
            lines[i] = lines[i][7:]
        quote += lines[i]
        i += 1
    notes = ''
    while (lines[i][:11] != 'Scripture: ' and
            lines[i][:6] != 'Talk: ' and
            lines[i][:7] != 'Quote: ' and 
            lines[i] != '\n'):
        if lines[i][:7] == 'Notes: ':
            lines[i] = lines[i][7:]
        notes += lines[i]
        i += 1
    entry = TalkEntry(topic=topic, talk=talk, quote=quote[:-1],
            notes=notes[:-1])
    entry.save()
    return i


def get_q_entry(lines, i, topic):
    quote = ''
    while (lines[i][:8] != 'Person: '):
        if lines[i][:7] == 'Quote: ':
            lines[i] = lines[i][7:]
        quote += lines[i]
        i += 1
    person = lines[i][8:-1]
    firstname, middlename, lastname, suffix = split_name(person)
    sid = Person.objects.get(firstname=firstname, middlename=middlename,
            lastname=lastname, suffix=suffix)
    i += 1
    source = lines[i][8:-1]
    i += 1
    notes = ''
    while (lines[i][:11] != 'Scripture: ' and
            lines[i][:6] != 'Talk: ' and
            lines[i][:7] != 'Quote: ' and
            lines[i] != '\n'):
        if lines[i][:7] == 'Notes: ':
            lines[i] = lines[i][7:]
        notes += lines[i]
        i += 1
    entry = Quote(topic=topic, quote=quote[:-1], person=sid,
            notes=notes[:-1], source=source)
    entry.save()
    return i

if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
