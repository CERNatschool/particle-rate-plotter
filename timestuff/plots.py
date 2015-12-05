#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

CERN@school: Data Profiling - Time Stuff - Plotting.

See http://cernatschool.web.cern.ch for more information.

"""

#...for the OS stuff.
import os

#...for the logging.
import logging as lg

#...for the time (being).
import time

#...for even more MATH.
import numpy as np

# Import the plotting libraries.
import pylab as plt

#...for the colours. Oh, the colours!
from matplotlib.colors import LogNorm

# Load the LaTeX text plot libraries.
from matplotlib import rc

# Uncomment to use LaTeX for the plot text.
#rc('font',**{'family':'serif','serif':['Computer Modern']})
#rc('text', usetex=True)

#...for plotting arbitrary rectangles on the plots.
from matplotlib.patches import Rectangle

#...for custom axis tickers.
import matplotlib.ticker as ticker

from handlers import make_time_dir

class MonthPlot:
    """ Wrapper class for the monthly plots. """

    def __init__(self, data_month, **kwargs):
        """
        Constructor.

        @param [in] data_month DataMonth object for the month to plot.
        """

        lg.info(" * Initialising MonthPlot object...")

        # Reset the matplot lib plotting stuff.
        plt.close()

        # Here we create the figure on which we'll be plotting our results.
        # We assign the figure a number, a size (5" x 3"), set the resolution
        # of the image (150 DPI), and set the background and outline to white.

        ## The figure width [inches].
        self.__fig_w = 5.0
        #
        if "fig_width" in kwargs.keys():
            self.__fig_width = kwargs["fig_width"]

        ## The figure height [inches].
        self.__fig_h = 5.0
        #
        if "fig_height" in kwargs.keys():
            self.__fig_h = kwargs["fig_height"]

        ## The histogram.
        self.__plot = plt.figure(101, figsize=(self.__fig_w, self.__fig_h), dpi=150, facecolor='w', edgecolor='w')

        # Then we give a bit of clearance for the axes.
        self.__plot.subplots_adjust(bottom=0.17, left=0.15)

        # This is the subplot on which we'll actually be plotting.
        self.__plot_ax = self.__plot.add_subplot(111)

        # Label your axes:

        ## The x axis label.
        self.__x_label = "Day"
        #
        if "x_label" in kwargs.keys():
            self.__x_label = kwargs["x_label"]
        #
        plt.xlabel(self.__x_label)

        ## The y axis label.
        self.__y_label = "$y$"
        #
        if "y_label" in kwargs.keys():
            self.__y_label = kwargs["y_label"]
        #
        plt.ylabel(self.__y_label)

        # Plot the number of frames.

        # Should be we use a logarithmic scale for the y axis?
        # Not yet, but we might do later.
        uselogy = False

        # Firstly, we'll choose our plot bin values. We will use bin
        # widths of 1.

        ## The maximum x (day) value.
        max_x = data_month.getNumberOfDays()
        #lg.info(" * x max                           : %4d" % (sim_max_x))

        ## The bin width - we'll stick with one for the moment.
        bin_width = 1

        # Create the bin edges array for the frames data:
        bins = np.arange(1, max_x+bin_width, bin_width)
        #lg.info("* Bins")
        #lg.info bins # uncomment this if you want to see the actual bin edges.
        lg.info(" *")

        #lg.info(" * Bins:")
        #lg.info(bins)
        #lg.info(" * Frames from each day:")
        #lg.info(data_month.getFramesInEachDay().values())
        #lg.info(" *")

        # Create a histogram for the frames data
        # using the bin edges defined above.
        #
        ## The bar chart patches.
        patches_f = plt.bar(bins, data_month.getFramesInEachDay().values())

        # Set the display propertied of the "patches" (bars).
        # We're using translucent green bars with no outline.
        plt.setp(patches_f, 'facecolor', '#AADDAA', 'alpha', 1.0, 'linewidth', 0.0)

        ## The maximum y value.
        y_max = max(data_month.getFramesInEachDay().values())
        #
        # Round up to the nearest 1000.
        y_max = 1000 * (np.floor(y_max/1000.) + 1)
        #
        if y_max > 0:
            plt.ylim([0.0, y_max])

        # If supplied by the user, set the y axis limits.
        if "y_max" in kwargs.keys():
            y_max = kwargs["y_max"]
            plt.ylim([0.0, y_max])

        # Shade out the unused days.
        self.__plot_ax.add_patch(Rectangle((data_month.getNumberOfDays() + 1, 0), 31 - data_month.getNumberOfDays(), y_max, facecolor="#dddddd", edgecolor="#dddddd"))

        # Add gridlines.
        plt.grid(1)

        ## The x axis maximum.
        self.__x_max = 32.0
        #
        if "x_max" in kwargs.keys():
            self.__x_max = kwargs["x_max"]

        # Set the x axis limits.
        plt.xlim([1, self.__x_max])

        lg.info(" *")

    def save_plot(self, outputpath, name):
        """ Saves the figure. """

        # PNG (for HTML pages).
        self.__plot.savefig(outputpath + "/%s.png" % (name))

        # PostScript (for publications).
        self.__plot.savefig(outputpath + "/%s.ps"  % (name))


class HourPlot:
    """ Wrapper class for the hourly plots. """

    def __init__(self, data_hour, **kwargs):
        """
        Constructor.
        """

        lg.info(" *")
        lg.info(" * Initialising HourPlot object...")
        #print(" * Initialising HourPlot object...")

        # Reset the matplot lib plotting stuff.
        plt.close()

        # Here we create the figure on which we'll be plotting our results.
        # We assign the figure a number, a size (5" x 3"), set the resolution
        # of the image (150 DPI), and set the background and outline to white.

        ## The figure width [inches].
        self.__fig_w = 42.0
        #
        if "fig_width" in kwargs.keys():
            self.__fig_width = kwargs["fig_width"]

        ## The figure height [inches].
        self.__fig_h = 4.2
        #
        if "fig_height" in kwargs.keys():
            self.__fig_h = kwargs["fig_height"]

        ## The histogram.
        self.__plot = plt.figure(101, figsize=(self.__fig_w, self.__fig_h), dpi=150, facecolor='w', edgecolor='w')

        # Then we give a bit of clearance for the axes.
        self.__plot.subplots_adjust(bottom=0.15, left=0.02, right=0.99)

        # This is the subplot on which we'll actually be plotting.
        self.__plot_ax = self.__plot.add_subplot(111)

        # Label your axes:

        ## The x axis label.
        self.__x_label = "$t$ / s"
        #
        if "x_label" in kwargs.keys():
            self.__x_label = kwargs["x_label"]
        #
        plt.xlabel(self.__x_label)

        ## The y axis label.
        self.__y_label = "$y$"
        #
        if "y_label" in kwargs.keys():
            self.__y_label = kwargs["y_label"]
        #
        plt.ylabel(self.__y_label)

        # Plot the number of frames.

        # Should be we use a logarithmic scale for the y axis?
        # Not yet, but we might do later.
        uselogy = False

        ## The hour's start time.
        h_st = data_hour.getStartTime()

        lg.info(" * The hour's start time: %d [s] => '%s' UTC." % (h_st, make_time_dir(h_st)))

        ## The maximum y value.
        y_max = 1.0

        # Loop over the frames found.
        for i, st in enumerate(data_hour.getStartTimes()):

            ## The frame's acquisition time [s].
            acq_time = data_hour.getAcqTimes()[i]

            ## The number of pixels in the frame.
            n_pixels = data_hour.getNumberOfPixels()[i]

            lg.info(" * Found new frame: %s (%f [s], % 7d pixels)." % (time.asctime(time.gmtime(st)), acq_time, n_pixels))

            ## The "normal" frame colour.
            frame_color = "#44aa44"

            ## The x position of the frame's bar (frame - hour's start time).
            x = st - h_st

            lg.info(" *--> Start time from frame: % 15d [s] => '%s' UTC." % (st, make_time_dir(st)))
            lg.info(" *--> %d, %d, %d" % (st, h_st, x))

            ## The y position of the frame's bar.
            y = 0

            ## The width of the bar - the acquition time.
            w = acq_time
            #
            ## The height of the bar - the pixels per second.
            #
            # This means the area of the bar is the total number of pixels
            # in the frame.
            if float(acq_time) > 0.:
                h = float(n_pixels) / float(acq_time)
            else:
                h = 500
                w = 1
                frame_color = "#222288"

            # Check if we have a noisy frame.
            if n_pixels > 30000:
                # Set the frame color to indicate an error (i.e. noise).
                frame_color = "#882222"
            else:
                # If normal, check if we have a new maximum.
                if h > y_max:
                    y_max = h

            lg.info(" *---> (x, y) = (%f, %f)" % (x, y))
            lg.info(" *---> (w, h) = (%f, %f)" % (w, h))

            # Add a rectangle representing the frame to the plot.
            self.__plot_ax.add_patch(Rectangle((x, y), w, h, facecolor=frame_color, edgecolor=frame_color))

        # Round up to the nearest 10.
        y_max = 10 * (np.floor(y_max/10.) + 1)
        #
        if y_max > 0:
            plt.ylim([0.0, y_max])

        # If supplied by the user, set the y axis limits.
        if "y_max" in kwargs.keys():
            y_max = kwargs["y_max"]
            plt.ylim([0.0, y_max])

        # Add gridlines.
        plt.grid(1)

        ## The x axis maximum.
        self.__x_max = 3600.0
        #
        if "x_max" in kwargs.keys():
            self.__x_max = kwargs["x_max"]

        # Set the x axis limits.
        plt.xlim([0, self.__x_max])

        # Set the x axis tickers.
        self.__plot_ax.xaxis.set_ticks(np.arange(0.0, self.__x_max + 100, 100))

        #self.__plot_ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))

        lg.info(" *")

    def save_plot(self, outputpath, name):
        """ Saves the figure. """

        # The PNG path (for HTML pages).
        png_path = os.path.join(outputpath, "%s.png" % (name))
        #
        self.__plot.savefig(png_path)

        ## The PostScript path (for publications).
        ps_path = os.path.join(outputpath, "%s.ps" % (name))
        #
        self.__plot.savefig(ps_path)

        print("* Saved figures '%s' and '%s'." % (png_path, ps_path))
        lg.info("* Saved figures '%s' and '%s'." % (png_path, ps_path))
