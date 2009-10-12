#!/usr/bin/env python

import urllib
from BeautifulSoup import BeautifulSoup
from studyjournal.talks.models import Person

def main():
    for person in Person.objects.all():
        if person.lastname == 'Other':
            continue
        link = 'http://www.gapages.com/'+link_from_name(person)
        file = urllib.urlopen(link)
        soup = BeautifulSoup(file)
        if '404 Not Found' in str(soup.title):
            print 'No page found for', person.name()
            print 'Tried:', link
            continue
        else:
            print 'Page found for', person.name(), ':', link
            person.ga_bio = link
            person.save()

def link_from_name(person):
    link = ''
    if len(person.lastname) < 5:
        link = person.lastname.lower()
    else:
        link = person.lastname[:5].lower()
    link += person.firstname[0].lower()
    if not person.middlename == '_':
        link += person.middlename[0].lower()
    link += '1.htm'
    return str(strip_accents(link))

def strip_accents(s):
    # Don't ask - I don't know.  I just found it online.
    import unicodedata
    return ''.join((c for c in unicodedata.normalize('NFD', s)
            if unicodedata.category(c) != 'Mn'))


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
