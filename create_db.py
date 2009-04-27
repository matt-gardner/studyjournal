#!/usr/bin/env python

from studyjournal.talks.models import Talk
from datetime import date

def main():
    create_people()
    create_talks()

def create_people():
    peoplefile = open('data/people.txt')
    person = None
    while True:
        line = peoplefile.readline()
        if not line:
            break
        line = line[:-1]
        if line[0] == ' ':
            fields = line.split(': ')
            callingname = fields[0].strip()
            dates = fields[1].split('-')
            sday, smonth, syear = dates[0].split('/')
            sdate = date(int(syear), int(smonth), int(sday))
            if dates[1] == 'present':
                edate = None
            else:
                eday, emonth, eyear = dates[1].split('/')
                edate = date(int(eyear), int(emonth), int(eday))
            if edate:
                person.calling_set.create(calling=callingname, startdate=sdate,
                        enddate=edate)
            else:
                person.calling_set.create(calling=callingname, startdate=sdate)
        else:
            name, gender = line.split(', ')
            person = Person(name=name, gender=gender)
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
        if line.isspace():
            break
        if not line:
            break
    text = ''
    for line in talkfile:
        text = text + line.decode('utf-8')
    day = int(day)
    year = int(year)
    month = get_month(month)
    d = date(year, month, day)
    talk = Talk(speaker=speaker, calling=calling, gender=gender, date=d,
            title=title, text=text, topic=topic, type=type)
    talk.save()

def get_month(month):
    if 'Jan' in month:
        m = 1
    elif 'Feb' in month:
        m = 2
    elif 'Mar' in month:
        m = 3
    elif 'Apr' in month:
        m = 4
    elif 'May' in month: 
        m = 5
    elif 'Jun' in month: 
        m = 6
    elif 'Jul' in month: 
        m = 7
    elif 'Aug' in month: 
        m = 8
    elif 'Sep' in month: 
        m = 9
    elif 'Oct' in month:
        m = 10
    elif 'Nov' in month:
        m = 11
    elif 'Dec' in month:
        m = 12
    return m


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
