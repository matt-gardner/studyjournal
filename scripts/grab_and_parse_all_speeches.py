#!/usr/bin/env python

from __future__ import division
from optparse import OptionParser
import urllib
from BeautifulSoup import BeautifulSoup, NavigableString
from remove_html_tags import get_html_sequences, remove_html_tags
from month import get_month_number
from name import split_name, remove_titles
from datetime import date
from studyjournal.talks.models import Talk, Person
import re

def main():
    parser = OptionParser()
    options, args = parser.parse_args()

    htmlsequences = get_html_sequences()
    baselink = 'http://speeches.byu.edu/?act=browse&speaker=%s,+%s+%s&topc=&type=&year=&x=14&y=8'
    basehttp = 'http://speeches.byu.edu/'

    # Go through each person in the data base
    for person in Person.objects.all():
        firstname, middlename, lastname, suffix = split_name(person.name())
        link = baselink % (lastname, firstname, middlename)

        # Get the base file from speeches.byu.edu - the file containing a list
        # of talks by a specific person - and open it for parsing.
        try:
            file = urllib.urlopen(link)
        except IOError:
            print "Couldn't find any talks for", person.name()
            continue
        except UnicodeError:
            print person.name(), "had a name that didn't work..."
            continue
        soup = BeautifulSoup(file)
        file.close()
        try:
            results = str(soup.find(name='span').findNext(name='p'))
        except AttributeError:
            results = ''
        if 'no results for your request' in results:
            print "Couldn't find any talks for", person.name()
            continue
        links = []
        # Grab all the talk links from the file - they all have this action in
        # their url
        r = re.compile(r'\?act=viewitem\&id=\d+$')
        for link in soup.findAll(name='a'):
            for attr in link.attrs:
                if attr[0] == 'href' and re.match(r, attr[1]):
                    links.append(link)
        # Grab each talk, find the relevant info about it, and enter it into the
        # database.
        for link in links:
            # A bunch of stuff can be grabbed from the link on the initial list
            # page
            url = basehttp+link.attrs[0][1]
            r = re.compile(r'\w+ \d+, \d+')
            try:
                d = re.search(r, link.contents[0]).group(0)
            except AttributeError:
                print "Couldn't find a date?  That's weird...  Moving on."
                continue
            d = d.replace(',','')
            month, day, year = d.split(' ')
            year = int(year)
            month = get_month_number(month)
            day = int(day)
            d = date(year, month, day)
            start = link.contents[0].find(')')+2
            end = link.contents[0].find('&gt;')-1
            title = link.contents[0][start:end]
            title = remove_html_tags(title, htmlsequences)
            t = 'BYU'
            # Grab the next page, which is a list of ways to view or buy the
            # talk. We want the html version, so grab that link from the page.
            file = urllib.urlopen(url)
            soup = BeautifulSoup(file)
            file.close()
            # Very cryptic, I know.  Sorry.  This is where the id is that you
            # need to pass to the reader so it knows what talk to display
            try:
                actuallink = basehttp+'reader/reader.php?id='+soup.find(
                        attrs={'name':'id', 'type':'hidden'}).attrs[2][1]
            except AttributeError:
                try:
                    Talk.objects.get(speaker=person, date=d, title=title,
                            text='', type=t, externallink=url)
                    print person.name()+',',title,'is already in the database!'
                except Talk.DoesNotExist:
                    print "Couldn't find text for",person.name()+',',title+'.'
                    print 'Adding talk without text'
                    talk = Talk(speaker=person, date=d, title=title, text='',
                            type=t, externallink=url)
                    talk.save()
                continue
            # Get the actual html page that contains the talk, and parse stuff
            # out of it.
            try:
                file = urllib.urlopen(actuallink)
                soup = BeautifulSoup(file)
                file.close()
                header = ''
                try:
                    header = ''.join(soup.findAll(name='i')[1].findAll(
                            text=True))
                except IndexError:
                    print 'No header...'
                if 'fireside' in header:
                    t = 'CES'
                text = header
                text += ''.join(soup.findAll(name='hr')[1].findAllNext(
                        text=True))
                text = remove_html_tags(text, htmlsequences)
                try:
                    Talk.objects.get(speaker=person, date=d, title=title,
                            type=t, externallink=actuallink)
                    print person.name()+',',title,'is already in the database!'
                except Talk.DoesNotExist:
                    talk = Talk(speaker=person, date=d, title=title, text=text,
                            type=t, externallink=actuallink)
                    print 'Added',person.name()+',',title
                    talk.save()
            except IndexError:
                print "Couldn't add",person.name()+',',title+'.'
                print "Something bad happened..."


def clean_file(outdir, filename):
    file = open(outdir+'index.html'+filename, 'U')
    newfile = open(outdir+filename,'w')
    for line in file:
        if '<head "' in line:
            newfile.write('<head>\n')
        else:
            newfile.write(line)
    file.close()
    newfile.close()
    


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
