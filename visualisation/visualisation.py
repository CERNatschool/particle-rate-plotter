#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Functions for visualising frames.
"""

#...for the MATH.
import numpy as np

#...for the plotting.
import pylab as plt

#...for the colours.
from matplotlib import colorbar, colors

#...for setting the axes ticks.
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


def makeFrameImage(basename, pixels, outputpath, pixel_mask = {}):
    """ Create the frame image. """

    # The frame limits.
    x_min = 0; x_max = 256; y_min = 0; y_max = 256

    ## The frame width.
    w = 256

    ## The frame height.
    h = 256

    # Remove the masked pixels.
    for X in pixel_mask.keys():
        if X in pixels.keys():
            del pixels[X]

    ## The maximum count value.
    C_max = max(pixels.values())

    # Create the figure.
    plt.close('all')

    figsize = 5.0

    ## The figure for the frame.
    frfig = plt.figure(1, figsize=(figsize*1.27, figsize), dpi=150, facecolor='w', edgecolor='w')

    ## The frame axes.
    frfigax = frfig.add_subplot(111, axisbg='#222222')

    # Add the frame background (blue).
    frfigax.add_patch(plt.Rectangle((0,0),256,256,facecolor='#82bcff'))

    # Add a grid.
    plt.grid(1)

    # Select the "hot" colour map for the pixel counts.

    cmap = plt.cm.hot

    colax, _ = colorbar.make_axes(plt.gca())

    col_max = 10*(np.floor(C_max/10.)+1)

    colorbar.ColorbarBase(colax,cmap=cmap,norm=colors.Normalize(vmin=0,vmax=col_max))

    # Loop over the pixels and plot them.
    for X, C in pixels.iteritems():
        x = X % 256; y = X / 256
        scaled_C = float(C)/float(col_max)
        frfigax.add_patch(plt.Rectangle((x,y),1,1,edgecolor=cmap(scaled_C),facecolor=cmap(scaled_C)))

    # Loop over the masked pixels and plot them.
    for X, C in pixel_mask.iteritems():
        x = X % 256; y = X / 256
        frfigax.add_patch(plt.Rectangle((x,y),1,1,edgecolor='#00CC44',facecolor='#00CC44'))

    # Set the axis limits based.
    b = 3 # border

    frfigax.set_xlim([0 - b, 256 + b])
    frfigax.set_ylim([0 - b, 256 + b])

    # Save the figure.
    frfig.savefig(outputpath + "/%s.png" % (basename))
