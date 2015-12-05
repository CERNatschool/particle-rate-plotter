#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Plotting functions for property histograms.
"""

#...for the logging.
import logging as lg

#...for the MATH.
import math

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

class Hist():
    """ Wrapper class for 1D property histograms. """

    def __init__(self, name, num, data, nbins, xlabel, ylabel, outputpath):

        plt.close('all')

        ## The property histogram plot.
        p = plt.figure(num, figsize=(5.0, 3.0), dpi=150, facecolor='w', edgecolor='w')

        # Adjust the position of the axes.
        p.subplots_adjust(bottom=0.17, left=0.15)

        ## The plot axes.
        pax = p.add_subplot(111)

        # y axis
        plt.ylabel('%s' % (ylabel))

        # x axis
        plt.xlabel('%s' % (xlabel))

        # Add a grid.
        plt.grid(1)

        ## The x minimum.
        xmin = 0

        ## The x maximum.
        xmax = max(data) + 5

        if nbins < 0:
            n, bins, patches = plt.hist(data, range(int(xmin),int(xmax),1), histtype='stepfilled')
        else:
            n, bins, patches = plt.hist(data, nbins, histtype='stepfilled')

        # Set the plot's visual properties.
        plt.setp(patches, 'facecolor', 'g', 'alpha', 0.75, 'linewidth', 0.0)

        # Save the figure.
        p.savefig("%s/%s.png" % (outputpath, name))

class Hist2D:
    """ Wrapper class for 2D property vs. property histograms. """

    def __init__(self, num, name, x_data, x_ax_label, x_nbins, y_data, y_ax_label, y_nbins, outputpath):

        plt.close('all')

        ## The histogram plot.
        plot = plt.figure(num, figsize=(5.0, 3.0), dpi=150, facecolor='w', edgecolor='w')

        # Adjust the position of the axes.
        plot.subplots_adjust(bottom=0.17, left=0.15)

        ## The plot axes.
        plotax = plot.add_subplot(111)

        # Set the y axis label.
        plt.ylabel(y_ax_label)

        # Set the x axis label.
        plt.xlabel(x_ax_label)

        # Add a grid.
        plt.grid(1)

        # Plot the 2D histogram.
        plt.hist2d(x_data, y_data, bins=[x_nbins, y_nbins], norm=LogNorm())

        # Add a colour bar.
        plt.colorbar()

        # Save the figure.
        plot.savefig("%s/%s.png" % (outputpath, name))
