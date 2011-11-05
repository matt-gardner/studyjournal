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

from dirutil import create_dirs_and_open
from month import get_month_number
from name import split_name, remove_titles
from remove_html_tags import get_html_sequences, remove_html_tags
from scrape import urlopen_with_chrome

from studyjournal.talks.models import Talk, Person

# NOTE:
# This will grab all audio files on a conference page, except for files labeled
# as whole sessions.  That means, for instance, that downloading audio in a
# language other than English will just grab talks, because they don't have
# download links for music in other languages.  But if you do this for English
# audio, it will grab music, too.  I don't have an option yet for just getting
# music or just getting talks.  It should be easy, I just haven't done it yet.

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
    print 'Grabbing general conference talks for date:',  d
    talks = soup.findAll('a', attrs={'class': 'audio-mp3'})
    links = []
    for t in talks:
        # We don't want to download the "whole session" audio files, so this
        # looks for those head rows and ignores them.
        tr = t.parent.parent.parent.parent.parent.parent
        if (tr.attrs and tr.attrs[0][0] == 'class'
                and tr.attrs[0][1] == 'head-row'):
            continue
        # The talks are a span that has an a inside of it, and the a has an
        # href attr.  a.attrs is the set of attributes of the a tag, the href
        # is first.  The attr itself is a tuple ('href', [link]), so we grab
        # the link.
        links.append(t.attrs[0][1])
    print 'Downloading audio for %d talks' % len(links)
    base = 'downloaded_audio/'
    for link in links:
        print 'Getting mp3:', link
        html = urlopen_with_chrome(link)
        filename = base + link.split("/")[-1].split('?')[0]
        print 'Saving file as:', filename
        f = create_dirs_and_open(filename)
        f.write(html)
        f.close()
    return


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
