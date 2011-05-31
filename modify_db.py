#!/usr/bin/env python

import os, sys

sys.path.append(os.curdir+'/../')
os.environ['DJANGO_SETTINGS_MODULE'] = 'studyjournal.settings'

from studyjournal.topicalguide.models import *
from studyjournal.talks.models import *
from django.contrib.auth.models import User

# vim: et sw=4 sts=4
