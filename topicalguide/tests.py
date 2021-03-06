"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from scriptures import get_link

class ScriptureTest(TestCase):
    def test_get_link(self):
        """
        A bunch of test cases for get_link.  It could probably use some more
        cases.
        """
        scriptures = ['Alma 42:9, 11, 14, 18 (the whole chapter is good)',
                'Alma 13:12-13, 16, 29',
                'Alma 13:6',
                '2 Nephi 32:7 (1-7)',
                'Mark 9:2 JST',
                '2 Corinthians 6:17-17:1',
                'Mosiah 23:21-22, 24:13-16',
                '1 Peter 1:8, Helaman 5:44',
                'Mosiah 17:2-4, 18:1-3',
                'Mosiah 27 (v. 24), 28:3-4',
                '1 Kings 3:9, 12, 4:29',
                'Matthew 7:6, 3 Nephi 14:6',
                'Luke 14:26 (JST), 33']
        correct = ['<a href="http://scriptures.lds.org/en/alma/42/9,11,14,18#9">Alma 42:9, 11, 14, 18 (the whole chapter is good)</a>',
            '<a href="http://scriptures.lds.org/en/alma/13/12-13,16,29#12">Alma 13:12-13, 16, 29</a>',
            '<a href="http://scriptures.lds.org/en/alma/13/6#6">Alma 13:6</a>',
            '<a href="http://scriptures.lds.org/en/2_ne/32/7#7">2 Nephi 32:7 (1-7)</a>',
            '<a href="http://scriptures.lds.org/en/mark/9/2#2">Mark 9:2 JST</a>',
            '<a href="http://scriptures.lds.org/en/2_cor/6/17#17">2 Corinthians 6:17-17:1</a>',
            '<a href="http://scriptures.lds.org/en/mosiah/23/21-22#21">Mosiah 23:21-22, </a><a href="http://scriptures.lds.org/en/mosiah/24/13-16#13">24:13-16</a>',
            '<a href="http://scriptures.lds.org/en/1_pet/1/8#8">1 Peter 1:8, </a><a href="http://scriptures.lds.org/en/hel/5/44#44">Helaman 5:44</a>',
            '<a href="http://scriptures.lds.org/en/mosiah/17/2-4#2">Mosiah 17:2-4, </a><a href="http://scriptures.lds.org/en/mosiah/18/1-3#1">18:1-3</a>',
            '<a href="http://scriptures.lds.org/en/mosiah/27">Mosiah 27 (v. 24), </a><a href="http://scriptures.lds.org/en/mosiah/28/3-4#3">28:3-4</a>',
            '<a href="http://scriptures.lds.org/en/1_kgs/3/9,12#9">1 Kings 3:9, 12, </a><a href="http://scriptures.lds.org/en/1_kgs/4/29#29">4:29</a>',
            '<a href="http://scriptures.lds.org/en/matt/7/6#6">Matthew 7:6, </a><a href="http://scriptures.lds.org/en/3_ne/14/6#6">3 Nephi 14:6</a>',
            '<a href="http://scriptures.lds.org/en/luke/14/26,33#26">Luke 14:26 (JST), 33</a>']
        for i, s in enumerate(scriptures):
            self.failUnlessEqual(get_link(s), correct[i])

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

