#!/usr/bin/env python

from studyjournal.talks.models import Talk, Person

def main():
    otherid = Person.objects.get(name='Other')
    for talk in Talk.objects.filter(speaker=otherid):
        try:
            sid = Person.objects.get(name=talk.speakername)
            talk.speaker = sid
            talk.speakername = ''
            talk.save()
        except Person.DoesNotExist:
            continue

if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
