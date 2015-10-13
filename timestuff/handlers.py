#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Handler methods for various time-related things.
"""

#...for the logging.
import logging as lg

#...for the regex module.
import re

#...for the time functionality.
import time

def isStartTimeStringValid(sts):
    """ Check the format of the time string. """

    # regex match for the start time string.
    r_starttime = re.compile(r'[A-Z][a-z][a-z] [A-Z][a-z][a-z] \d{2,2} \d{2,2}:\d{2,2}:\d{2,2}.\d{6,6} \d{4,4}')

    if r_starttime.match(sts) is not None:
        return True
    else:
        return False

def getPixelmanTimeString(st):
    """ Get the timestring in the Pixelman (custom) format. """

    ## The seconds from the start time provided.
    sec = int(str(st).split(".")[0])

    ## The seb-second value.
    #sub = int(("%.7f" % st).strip().split(".")[1])
    sub = ("%.6f" % st).strip().split(".")[1]

    ## The time represented as a Python time object.
    mytime = time.gmtime(sec)

    ## The time in the Pixelman format.
    #sts = time.strftime("%a %b %d %H:%M:%S.", mytime) + ("%06d" % (sub)) + time.strftime(" %Y", mytime)
    sts = time.strftime("%a %b %d %H:%M:%S.", mytime) + ("%s" % (sub)) + time.strftime(" %Y", mytime)

    return sec, sub, sts


def make_time_dir(sec):

    ## The time represented as a Python time object.
    mytime = time.gmtime(sec)

    ## The time in the directory format.
    s = time.strftime("%Y-%m-%d-%H%M%S", mytime)

    return s
