#!/usr/bin/env python

from studyjournal.talks.models import Person, Calling
from datetime import date

def main():
    peoplefile = open('people.txt')
    person = None
    while True:
        line = peoplefile.readline()
        if not line:
            break
        line = line[:-1]
        if line[0] == ' ':
            fields = line.split(': ')
            callingname = fields[0]
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
            person = Person(name=line, gender='M')
            person.save()


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
