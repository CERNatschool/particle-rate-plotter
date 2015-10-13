#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

CERN@school: Data Profiling - Time Stuff - Wrappers.

See http://cernatschool.web.cern.ch for more information.

"""

#...for the logging.
import logging as lg

#...for the time (being).
import time

#...for the custom Pixelman time string.
from handlers import getPixelmanTimeString, make_time_dir

class DataMonth:
    """ Wrapper class for each month. """

    def __init__(self, start_time_s, end_time_s):
        """ Constructor. """

        lg.info(" * Initialising DataMonth object...")

        ## The start time of the month [s].
        self.__st_s = start_time_s

        ## The Python time object representing the month start time.
        self.__st = time.gmtime(self.__st_s)

        ## The Pixelman time string of the start time.
        self.__st_str = getPixelmanTimeString(self.__st_s)[2]

        ## The end time of the month [s].
        self.__et_s = end_time_s

        ## The Python time object representing the month end time.
        self.__et = time.gmtime(self.__et_s)

        ## The Pixelman time string of the end time.
        self.__et_str = getPixelmanTimeString(self.__et_s)[2]

        ## The duration of the month [s].
        self.__Delta_s = self.__et_s - self.__st_s + 1

        ## The number of non-full day seconds in the month (error checking).
        self.__remainder_seconds = self.__Delta_s % (60 * 60 * 24)

        ## The number of days in the month [days].
        self.__n_days = (self.__Delta_s - self.__remainder_seconds) / (60 * 60 * 24)
        #
        if self.__remainder_seconds != 0:
            raise IOError("* Error! Month has %d remainder seconds." % (self.__remainder_seconds))

        ## Dictionary of the number of frames recorded in each day.
        self.__frames_in_a_day = {}
        #
        #
        for day in range(1, self.__n_days + 1):
            self.__frames_in_a_day[day] = 0

        ## The number of frames found in that month.
        self.__num_frames = 0

        # Update the user.
        lg.info(" * Start time is %s (%d)" % (self.__st_str, self.__st_s))
        lg.info(" * End   time is %s (%d)" % (self.__et_str, self.__et_s))
        lg.info(" * Number of days in the month = %d" % (self.__n_days))
        lg.info(" *")

    def __lt__(self, other):
        return self.getStartTime() < other.getStartTime()

    def getStartTime(self):
        return self.__st_s

    def getNumberOfDays(self):
        return self.__n_days

    def getName(self):
        return time.strftime("%Y-%m", self.__st)

    def addFrame(self, st):
        """
        Add a frame to the month.

        @param [in] st The frame start time [s].
        """
        self.__num_frames += 1

        ## The day of the month (%02d) associated with the start time.
        day = int(time.strftime("%d", time.gmtime(st)))

        #lg.info(" * Found new frame: %s -> day = %d" % (time.asctime(time.gmtime(st)), day))

        self.__frames_in_a_day[day] += 1

    def getNumberOfFrames(self):
        return self.__num_frames

    def getFramesInEachDay(self):
        return self.__frames_in_a_day


class DataDay:
    """ Wrapper class for each day. """

    def __init__(self, start_time_s, end_time_s):
        """ Constructor. """

        lg.info(" *")
        lg.info(" * Initialising DataDay object...")

        ## The start time of the day [s].
        self.__st_s = start_time_s

        lg.info(" *--> Start time is % 15d [s] => '%s' UTC." % (self.__st_s, make_time_dir(self.__st_s)))

        ## The Python time object representing the day start time.
        self.__st = time.gmtime(self.__st_s)

        ## The Pixelman time string of the start time.
        self.__st_str = getPixelmanTimeString(self.__st_s)[2]

        ## The end time of the day [s].
        self.__et_s = end_time_s

        ## The Python time object representing the month end time.
        self.__et = time.gmtime(self.__et_s)

        ## The Pixelman time string of the end time.
        self.__et_str = getPixelmanTimeString(self.__et_s)[2]

        ## The duration of the day [s].
        self.__Delta_s = self.__et_s - self.__st_s + 1

        ## The number of non-full hour seconds in the day (error checking).
        self.__remainder_seconds = int(self.__Delta_s % (60 * 60))

        ## The number of hours in the day [hours].
        self.__n_hours = int((self.__Delta_s - self.__remainder_seconds) / (60 * 60))
        #
        if self.__remainder_seconds != 0:
            raise IOError("* Error! Day has %d remainder seconds." % (self.__remainder_seconds))

        ## Dictionary of the number of frames recorded in each day.
        self.__frames_in_an_hour = {}
        #
        ## Dictionary of the hours in the day.
        self.__hours = {}
        #
        for hour in range(self.__n_hours):

            self.__frames_in_an_hour[hour] = 0

            self.__hours[hour] = DataHour(self.__st_s + (hour*60*60), self.__st_s + ((hour+1)*60*60) - 1)

        ## The number of frames found in that day.
        self.__num_frames = 0

        # Update the user.
        lg.info(" * Start time is %s (%d)" % (self.__st_str, self.__st_s))
        lg.info(" * End   time is %s (%d)" % (self.__et_str, self.__et_s))
        lg.info(" * Number of hours in the day = %d" % (self.__n_hours))
        lg.info(" *")

    def __lt__(self, other):
        return self.getStartTime() < other.getStartTime()

    def getStartTime(self):
        return self.__st_s

    def getNumberOfHours(self):
        return self.__n_hours

    def getName(self):
        return time.strftime("%Y-%m-%d", self.__st)

    def addFrame(self, st, acq_time, n_pixels):
        """
        Add a frame to the day.

        @param [in] st The frame start time [s].
        @param [in] acq_time The frame acquisition time [s].
        @param [in] n_pixels The number of hit pixels in the frame.
        """
        self.__num_frames += 1

        ## The hour of the day (%02d) associated with the start time.
        hour = int(time.strftime("%H", time.gmtime(st)))

        # Add the frame to the day's hour.
        self.__hours[hour].addFrame(st, acq_time, n_pixels)

        #lg.info(" * Found new frame: %s -> hour = %d" % (time.asctime(time.gmtime(st)), hour))

        self.__frames_in_an_hour[hour] += 1

    def getNumberOfFrames(self):
        return self.__num_frames

    def getFramesInEachHour(self):
        return self.__frames_in_an_hour

    def getHour(self, hour):
        return self.__hours[hour]


class DataHour:
    """ Wrapper class for each hour. """

    def __init__(self, start_time_s, end_time_s):
        """ Constructor. """

        lg.info(" *")
        lg.info(" * Initialising DataHour object...")

        ## The start time of the hour [s].
        self.__st_s = start_time_s

        ## The Python time object representing the hour's start time.
        self.__st = time.gmtime(self.__st_s)

        ## The Pixelman time string of the start time.
        self.__st_str = getPixelmanTimeString(self.__st_s)[2]

        ## The end time of the hour [s].
        self.__et_s = end_time_s

        ## The Python time object representing the hour's end time.
        self.__et = time.gmtime(self.__et_s)

        ## The Pixelman time string of the end time.
        self.__et_str = getPixelmanTimeString(self.__et_s)[2]

        ## The duration of the hour [s].
        self.__Delta_s = self.__et_s - self.__st_s + 1

        ## The number of non-minute hour seconds in the hour (error checking).
        self.__remainder_seconds = int(self.__Delta_s % 60)

        ## The number of minutes in the day [hours].
        self.__n_minutes = int((self.__Delta_s - self.__remainder_seconds) / 60)
        #
        if self.__remainder_seconds != 0:
            raise IOError("* Error! Hour has %d remainder seconds." % (self.__remainder_seconds))

        ## List of frame start times.
        self.__f_sts = []

        ## A list of frame acquisition times.
        self.__f_ats = []

        ## A list of the number of pixels in each frame.
        self.__f_nps = []

        ## The number of frames found in that hour.
        self.__num_frames = 0

        # Update the user.
        lg.info(" * Start time is %s (%d)" % (self.__st_str, self.__st_s))
        lg.info(" * End   time is %s (%d)" % (self.__et_str, self.__et_s))
        lg.info(" * Number of minutes in the hour = %d" % (self.__n_minutes))
        lg.info(" *")

    def __lt__(self, other):
        return self.getStartTime() < other.getStartTime()

    def getStartTime(self):
        return self.__st_s

    def getNumberOfMinutes(self):
        return self.__n_minutes

    def getName(self):
        return time.strftime("%Y-%m-%d-%H%M%S", self.__st)

    def addFrame(self, st, acq_time, n_pixels):
        """
        Add a frame to the hour.

        @param [in] st The frame start time [s].
        @param [in] acq_time The frame acquisition time [s].
        @param [in] n_pixels The number of hit pixels in the frame.
        """

        self.__num_frames += 1

        # Add the frame data.
        self.__f_sts.append(st)
        #
        self.__f_ats.append(acq_time)
        #
        self.__f_nps.append(n_pixels)
        #
        #lg.info(" * Found new frame: %s (%f [s], % 7d pixels)." % (time.asctime(time.gmtime(st)), acq_time, n_pixels))

    def getNumberOfFrames(self):
        return self.__num_frames

    def getStartTimes(self):
        return self.__f_sts

    def getAcqTimes(self):
        return self.__f_ats

    def getNumberOfPixels(self):
        return self.__f_nps
