#!/usr/bin/env python

from studyjournal.talks.models import Talk
from datetime import date

def main():
    indexfile = '/aml/data/mjg82/nlpdata/talks/indices/all/all.txt'
    basedir = '/aml/data/mjg82/nlpdata/talks/'
    f = open(indexfile)
    for file in f:
        if 'unparseable' in file:
            continue
        talkfile = open(basedir+file[:-1])
        try:
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
            if not gender:
                gender = 'M'
            if not title:
                title = ''
            if not topic:
                topic = ''
            if not day:
                day = 1
            else:
                day = int(day)
            year = int(year)
            if 'Jan' in month:
                month = 1
            elif 'Feb' in month:
                month = 2
            elif 'Mar' in month:
                month = 3
            elif 'Apr' in month:
                month = 4
            elif 'May' in month: 
                month = 5
            elif 'Jun' in month: 
                month = 6
            elif 'Jul' in month: 
                month = 7
            elif 'Aug' in month: 
                month = 8
            elif 'Sep' in month: 
                month = 9
            elif 'Oct' in month:
                month = 10
            elif 'Nov' in month:
                month = 11
            elif 'Dec' in month:
                month = 12
            d = date(year, month, day)
            talk = Talk(speaker=speaker, calling=calling, gender=gender, date=d,
                    title=title, text=text, topic=topic, type=type)
            talk.save()
        except (TypeError, ValueError), e:
            print 'Error in parsing talk',file[:-1]
            print str(e)
            continue



if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
