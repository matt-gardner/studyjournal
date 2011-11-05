#!/usr/bin/env python

from __future__ import division

import os, sys

sys.path.append(os.curdir+'/../')
os.environ['DJANGO_SETTINGS_MODULE'] = 'studyjournal.settings'

import re
from BeautifulSoup import BeautifulSoup, NavigableString
from datetime import date
from optparse import OptionParser
from subprocess import Popen
from sys import stdin

from month import get_month_number
from name import split_name, remove_titles
from remove_html_tags import get_html_sequences, remove_html_tags
from scrape import urlopen_with_chrome

from studyjournal.talks.models import Talk, Person

# WARNING!!!  I'm using BeautifulSoup for most of this, but I have modified
# BeautifulSoup!  Only a little bit, and it only affects spacing of things, but
# you should be aware that if you don't have those modifications to
# BeautifulSoup you will get different results than I do (or if you reinstall a
# machine, or update the package, or something).
#
# The modifications I made were found here:
# http://bazaar.launchpad.net/~mjumbewu/beautifulsoup/text-white-space-fix/revision/45
#
# The gist is that in the getText() method of BeautifulSoup.py, I took out a
# call to strip() and added a regular expression substitution of whitespace to
# collapse all strings of whitespace into a single space character.
#
# The effect of this change is that I have to call .strip() more often in my
# code, but when I call the .text method after a findAll, the whitespace is
# preserved correctly.

def main():
    parser = OptionParser()
    parser.add_option('-b','--base-link',
            dest='baselink',
            default=None,
            help='The base link for the conference proceedings on lds.org',
            )
    parser.add_option('-t','--test-run',
            dest='test_run',
            default=False,
            action='store_true',
            help='Do a test run, without actually committing anything to the '
            'database, to see how it goes',
            )
    options, args = parser.parse_args()

    htmlsequences = get_html_sequences()
    text_regex = re.compile(r'/general-conference/')

    html = urlopen_with_chrome(options.baselink)
    soup = BeautifulSoup(html)

    # The title is formatted like: "April 2011 General Conference LDS.org"
    d = soup.title.contents[0].split()
    month, year = d[0], d[1]
    year = int(year)
    month = get_month_number(month)
    day = 1
    d = date(year, month, day)
    type = 'GC'
    print 'Grabbing general conference talks for date:',  d
    talks = soup.findAll('span', attrs={'class': 'talk'})
    print 'I found %d talks in this general conference' % len(talks)
    links = []
    for t in talks:
        # The talks are a span that has an a inside of it, and the a has an
        # href attr.  a.attrs is the set of attributes of the a tag, the href
        # is first.  The attr itself is a tuple ('href', [link]), so we grab
        # the link.
        links.append(t.a.attrs[0][1])
    for link in links:
        html = urlopen_with_chrome(link)
        soup = BeautifulSoup(html)
        # The title is found in the only h1 on the page
        title = soup.find('h1').text.strip()
        title = remove_html_tags(title, htmlsequences)
        # The name is found inside of an h2 of class author.  BeautifulSoup
        # parses it wrong, though, probably thinking that a <p> cannot be
        # inside of an <h2>.  So we use findNext instead of find.
        name_soup = soup.find('h2', attrs={'class': 'author'}).findNext('a')
        name = remove_titles(name_soup.text.strip())
        name = remove_html_tags(name, htmlsequences)
        firstname, middlename, lastname, suffix = split_name(name)
        # The calling of the person is right after the name, inside a <p>
        # We don't actually do anything with the calling, here, though.  I
        # guess this is just in case you were wondering =).
        calling = name_soup.findNext('p').text.strip()
        # The text is in a set of paragraphs, each of which has a uri tag.  We
        # grab all of the paragraphs, then get the text from each one and join
        # it together with appropriate spacing
        text_soup = soup.findAll('p', attrs={'uri': text_regex})
        text_parts = []
        # This is more complicated than I would like it to be.  When there are
        # subheadings in the text, they show up as <h2>'s right before one of
        # these <p>'s.  So look for subheadings and add them in the right place
        # if they're there.
        seen_headings = set()
        for t in text_soup:
            prev = t.findPreviousSibling('h2')
            if prev:
                sub_heading = prev.text
                if sub_heading not in seen_headings:
                    text_parts.append(sub_heading)
                    seen_headings.add(sub_heading)
            text_parts.append(t.text.strip())
        text = '\n\n'.join([t for t in text_parts])
        footnote_soup = soup.findAll('li', attrs={'class': 'footnote '})
        footnotes = '\n\n'.join([f.text.strip() for f in footnote_soup])
        if footnotes:
            text += '\n\n' + footnotes
        # I'm not sure that the new lds.org uses html tags, but we do this just
        # in case
        text = remove_html_tags(text, htmlsequences)
        try:
            speaker = Person.objects.get(firstname=firstname,
                    middlename=middlename, lastname=lastname, suffix=suffix)
        except Person.DoesNotExist:
            print "Didn't find", name
            print "Try a different name?"
            input = stdin.readline()
            if input == 'no\n':
                continue
            elif input == 'add\n':
                pass
            else:
                name = input[:-1]
            firstname, middlename, lastname, suffix = split_name(name)
            try:
                speaker = Person.objects.get(firstname=firstname,
                        middlename=middlename, lastname=lastname, suffix=suffix)
                print 'Found', speaker.name(), 'in the database'
            except Person.DoesNotExist:
                speaker = Person(firstname=firstname, middlename=middlename,
                        lastname=lastname, suffix=suffix)
                if not options.test_run:
                    speaker.save()
                    print 'Adding', speaker.name(), 'to the database'
                else:
                    print 'Would have added', speaker.name(), 'to the database'
        try:
            Talk.objects.get(speaker=speaker, date=d, title=title, type=type,
                    externallink=link)
            print speaker.name() + ',', title, 'is already in the database'
        except Talk.DoesNotExist:
            talk = Talk(speaker=speaker, date=d, title=title, text=text,
                    type=type, externallink=link)
            if not options.test_run:
                talk.save()
                print 'Added %s, %s' % (name, title)
            else:
                print 'Would have added %s, %s' % (name, title)


    


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
