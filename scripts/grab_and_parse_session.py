#!/usr/bin/env python

from __future__ import division
from optparse import OptionParser
from subprocess import Popen
from BeautifulSoup import BeautifulSoup, NavigableString
from remove_html_tags import get_html_sequences, remove_html_tags
from month import get_month_number
from name import split_name, remove_titles
from datetime import date
from studyjournal.talks.models import Talk, Person
from sys import stdin

def main():
    parser = OptionParser()
    parser.add_option('-b','--base-link',
            dest='baselink',
            default=None,
            help='The base link for the conference proceedings on lds.org',
            )
    parser.add_option('-o','--outdir',
            dest='outdir',
            default=None,
            help='The place to put all of the downloaded talks',
            )
    parser.add_option('','--db',
            dest='database',
            default=False,
            action='store_true',
            help='Insert the talks directly into the database',
            )
    options, args = parser.parse_args()

    devnull = open('/dev/null','w')
    outdir = options.outdir

    get_proc = Popen(('wget',options.baselink), stdout=devnull, stderr=devnull,
            cwd=outdir)
    get_proc.wait()

    htmlsequences = get_html_sequences()
    basehttp = 'http://lds.org'
    filename = options.baselink.split('/')[-1]
    file = open(outdir+filename)
    soup = BeautifulSoup(file)
    file.close()
    d = soup.title.contents[0].strip().split(',')[1].strip()
    month, year = d.split(' ')
    year = int(year)
    month = get_month_number(month)
    day = 1
    d = date(year, month, day)
    t = 'GC'
    talks = soup.findAll(id='conference')
    links = []
    for i in [a*2 for a in range(len(talks)/2)]:
        if i == 0:
            continue
        links.append(basehttp+talks[i].parent.attrs[0][1])
    for link in links:
        get_proc = Popen(('wget',link), stdout=devnull, stderr=devnull,
                cwd=outdir)
        get_proc.wait()
        filename = link.split('/')[-1]
        file = open(outdir+filename)
        soup = BeautifulSoup(file)
        file.close()
        title = soup.findAll(id='conference')[2].h1.contents[0]
        if not isinstance(title, NavigableString):
            title = title.contents[0]
        title = remove_html_tags(title, htmlsequences)
        name = soup.findAll(id='conference')[3].p.contents[0].strip()
        name = remove_titles(name)
        name = remove_html_tags(name, htmlsequences)
        firstname, middlename, lastname, suffix = split_name(name)
        calling = soup.findAll(id='conference')[3].p.contents[2].contents[0]
        if len(calling.contents) == 1:
            calling = calling.contents[0]
        else:
            calling = 'President of the Church'
        text = ''.join(soup.findAll(id='conference')[3].findAll(text=True)[2:])
        text = remove_html_tags(text, htmlsequences)
        try:
            sid = Person.objects.get(firstname=firstname, middlename=middlename,
                    lastname=lastname, suffix=suffix)
            talk = Talk(speaker=sid, date=d, title=title, text=text, type=t,
                    externallink=link)
        except Person.DoesNotExist:
            print "Didn't find", name
            print "Try a different name?"
            input = stdin.readline()
            if input == 'no\n':
                continue
            elif input == '\n':
                sid = Person.objects.get(firstname='Other')
                talk = Talk(speaker=sid, speakername=name, date=d, title=title, 
                        text=text, type=t, externallink=link)
                print 'Added',name+',',title
                talk.save()
                continue
            else:
                name = input[:-1]
            firstname, middlename, lastname, suffix = split_name(name)
            try:
                sid = Person.objects.get(firstname=firstname, middlename=middlename,
                        lastname=lastname, suffix=suffix)
                talk = Talk(speaker=sid, date=d, title=title, text=text, type=t,
                        externallink=link)
            except Person.DoesNotExist:
                sid = Person.objects.get(firstname='Other')
                talk = Talk(speaker=sid, speakername=name, date=d, title=title, 
                        text=text, type=t, externallink=link)
        print 'Added',name+',',title
        talk.save()


    


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
