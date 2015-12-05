#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 CERN@school - Plotting the hit pixel profile from a binary file.

 See the README.md file and the GitHub wiki for more information.

 http://cernatschool.web.cern.ch

"""

# Import the code needed to manage files.
import os, glob

#...for parsing the arguments.
import argparse

#...for the logging.
import logging as lg

#...for the data unpacking.
import struct

#...for the MATH.
import math

#...for the file writing.
import codecs

#...for the time (being).
import time

#...for the extra time (stuff).
#
from timestuff.constants import *
#
from timestuff.wrappers import DataDay
#
from timestuff.plots import HourPlot
#
from timestuff.handlers import make_time_dir
#
from timestuff.pages import make_day_plot_page


if __name__ == "__main__":

    print("*")
    print("*==========================================*")
    print("* CERN@school - plot the hit pixel profile *")
    print("*==========================================*")

    # Get the datafile path from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("inputPath",       help="Path to the binary input data.")
    parser.add_argument("outputPath",      help="The path for the output files.")
    parser.add_argument("day",             help="The day to plot for.")
    parser.add_argument("numFrames",       help="The number of frames to process (-1 for all).")
    parser.add_argument("startFrame",      help="The starting frame.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The path to the data file.
    datapath = args.inputPath
    #
    # Check if the input file exists. If it doesn't, quit.
    if not os.path.exists(datapath):
        raise IOError("* ERROR: '%s' input file does not exist!" % (datapath))

    ## The output path.
    outputpath = args.outputPath
    #
    # Check if the output directory exists. If it doesn't, quit.
    if not os.path.isdir(outputpath):
        raise IOError("* ERROR: '%s' output directory does not exist!" % (outputpath))

    ## The day to plot.
    day_string = args.day
    #
    ## Time object for the day's start time.
    day_t = time.strptime(day_string, "%Y-%m-%d-%Z")

    ## String representing the day's start time.
    day_str = time.asctime(day_t)

    ## The start time (seconds since epoch) of the specified day [s].
    day_start_s = time.mktime(day_t)

    ## The end time (seconds since epoch) of the specified day [s].
    day_end_s = day_start_s + (SECONDS_IN_A_MINUTE * MINUTES_IN_AN_HOUR * HOURS_IN_A_DAY) - 1

    ## The day's output directory.
    day_output_path = os.path.join(outputpath, day_string)
    #
    if not os.path.isdir(day_output_path):
        os.mkdir(day_output_path)

    ## The number of frames to process.
    n_frames_to_process = int(args.numFrames)

    ## The start frame.
    start_frame_number = int(args.startFrame)

    # Set the logging level.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    # Configure the logging.
    lg.basicConfig(filename=os.path.join(outputpath, 'log_profile-data-by-day.log'), filemode='w', level=level)

    print("*")
    print("* Input path          : '%s'" % (datapath))
    print("* Output path         : '%s'" % (outputpath))
    print("*")
    print("* Day                 : %s" % (day_str))
    print("*")

    ## The total number of frames.
    n_frames = os.path.getsize(datapath) / 8

    # Error handling.
    if n_frames_to_process == -1:
        n_frames_to_process = n_frames
    #
    if start_frame_number > n_frames:
        raise IOError("* ERROR! Starting frame number greater than the number of frames.")

    lg.info(" * Plotting information about %s from '%s'" % (day_str, datapath))
    lg.info(" *")
    lg.info(" * File size                : % 15d [B]" % (os.path.getsize(datapath)))
    lg.info(" * Number of frames         : % 15d"     % (n_frames))

    ## The day to profile.
    my_day = DataDay(day_start_s, day_end_s)

    # Read the information from the binary dataset profile.
    with open(datapath, "rb") as bf:

        ## The frame count.
        frame_count = 0

        while True:

            ## The eight bytes representing the next frame.
            bs = bf.read(8)

            # Skip frames before the start frame (FIXME).
            if frame_count < start_frame_number:
                frame_count += 1
                continue

            # Quit if we're at the end of the file or frame count.
            if not bs or frame_count > (n_frames_to_process + start_frame_number - 1): break

            ## The frame's data - 8 bytes, eh? Nice.
            data = struct.unpack("IhH", bs)

            ## The start time (seconds since epoch) - 4 byte unsigned integer.
            start_time_s = data[0]

            lg.info(" *--> Frame start time %15d [s] -> '%s' (UTC)" % (start_time_s, make_time_dir(start_time_s)))

            ## The acquisition time (decoded 2 byte signed integer).
            #acq_time = math.pow(10, int(data[1]))
            acq_time = int(data[1])

            ## The number of hit pixels (2 byte unsigned integer).
            n_pixels = int(data[2])

            # Check if the start time is within the day.
            if day_start_s <= start_time_s <= day_end_s:
                my_day.addFrame(start_time_s, acq_time, n_pixels)

            frame_count += 1

    ## The number of frames processed - check.
    n_frames_check = 0

    ## Dictionary of the hour plots.
    hour_plots = {}

    # Loop over the hours in the day.
    #
    for hour, frames in my_day.getFramesInEachHour().iteritems():
        #
        n_frames_check += frames
        #
        lg.info(" * Frames in hour %02d: % 10d" % (hour, frames))

        ## The start time of the hour.
        hour_start_time_s = my_day.getHour(hour).getStartTime()

        # Get the hour start time.
        lg.info(" * Hour %02d start time % 15d [s] => '%s' UTC." % (hour, hour_start_time_s, make_time_dir(hour_start_time_s)))

        # Make the plot for the hour.
        hour_plots[hour] = HourPlot(my_day.getHour(hour), y_label="Pixels per second / [s -1]")
        #hour_plots[hour] = HourPlot(my_day.getHour(hour), y_label="Pixels per second / [$\\textrm{s}^{-1}$]")
        #hour_plots[hour] = HourPlot(my_day.getHour(hour), y_label="Pixels per second / [$\\textrm{s}^{-1}$]", y_max=30)

        # Save the profile plot to the output directory.
        hour_plots[hour].save_plot(day_output_path, hour)

        #break

    # Make the web page.

    ## Dictionary for the plot images.
    plot_paths = {}
    #
    for fn in sorted(glob.glob(os.path.join(day_output_path, "*.png"))):

        ## The hour number ("%H").
        hour = int(os.path.basename(fn).split(".")[0])
        #
        # Add the plot to the dictionary.
        plot_paths[hour] = os.path.basename(fn)

    #print plot_paths

    ## The path to the HTML page for the dataset profiles.
    html_path = os.path.join(day_output_path, "pixel-profile.html")
    #
    with codecs.open(html_path, 'w', 'utf-8') as f:
        f.write(make_day_plot_page(plot_paths))

    print("* Profile plots made for %s." % (day_str))
    print("* These can be viewed with the following command:")
    print("* $ firefox %s &" % (html_path))
