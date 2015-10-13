#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Plotting functions for property histograms.
"""

#...for the logging.
import logging as lg

#...for even more MATH.
import numpy as np

#...for the factorial function.
from scipy.misc import factorial

#...for the least squares fitting.
from scipy import optimize

# Import the plotting libraries.
import pylab as plt

#...for the colours. Oh, the colours!
from matplotlib.colors import LogNorm

# Load the LaTeX text plot libraries.
from matplotlib import rc

# Uncomment to use LaTeX for the plot text.
rc('font',**{'family':'serif','serif':['Computer Modern']})
rc('text', usetex=True)

#...for the chi^2 method.
from plotting.stats import chi2

class RateHistogram():

    def __init__(self, num, name, outputpath, dbg=False):
        """
        Plot the number of particles per frame and compare to the Poisson.
        """
        ## The number of the histogram (for book-keeping purposes).
        self.__num = num

        ## The name of the histogram.
        self.__name = name

        ## The output path for the plot.
        self.__output_path = outputpath

        ## Are we in debug mode?
        self.__dbg = dbg

        ## Bin width.
        self.bin_w = 1

        self.plot = plt.figure(self.__num, figsize=(5.0, 3.0), dpi=150, facecolor='w', edgecolor='w')

        self.plot.subplots_adjust(bottom=0.17, left=0.15)

        self.ax = self.plot.add_subplot(111)

        self.ax.set_xlabel("Clusters per frame")

        self.ax.set_ylabel("Number of frames")

        self.ax.grid(1)

        lg.info(" *")
        lg.info(" * Initialising a rate histogram '%s' (%d)" % (self.__name, self.__num))
        lg.info(" *")

    def fill(self, cpf):
        """
        Fill the histogram using a list of numbers and compare
        with the Poisson.
        @param [in] A list of the clusters per frame.
        """

        lg.info(" *")
        lg.info(" * Starting the fill routine for RateHistogram.")
        lg.info(" *")

        ## A list of the clusters per frame.
        self.__cpf = cpf

        ## The number of frames.
        self.__n_f = len(self.__cpf)

        ## The total number of clusters.
        self.__n_k = sum(self.__cpf)

        ## The estimated overall rate.
        self.__Lambda_est = float(self.__n_k) / float(self.__n_f)

        ## The standard error on the estimated overall rate.
        self.__Lambda_est_err = np.sqrt(float(self.__n_k)) / float(self.__n_f)

        lg.info(" * Number of frames supplied    (N)   = %d" % (self.__n_f))
        lg.info(" * The total number of clusters (M)   = %d" % (self.__n_k))
        lg.info(" *")
        lg.info(" * => \Lambda = (%f +- %f) [particles per unit time]" % (self.__Lambda_est, self.__Lambda_est_err))
        lg.info(" *")

        # Work out the bin details.
        self.max_x = max(self.__cpf)

        # Round this up to the nearest 10.
        self.max_x_r = np.floor(float(self.max_x)/10.) * 10. + 10.

        # Create the bin edges array for the data:
        # * Bin width one, rounded-up max x value.
        self.bins = np.arange(0, self.max_x_r + self.bin_w, self.bin_w)

        # Plot the histogram.

        ## A list of the histogram bin contents (n).
        self.__n = None

        ## A list of the histogram bins.
        self.__bins = None

        #self.n, self.bins, self.patches = plt.hist(self.cpf, bins=self.bins, histtype='stepfilled')
        self.__n, self.__bins = np.histogram(self.__cpf, bins=self.bins)

        lg.info(" * The histogram bin contents:")
        lg.info(self.__n)
        lg.info(" *--> Total number of frames (check): %d" % (sum(self.__n)))
        lg.info(" *")

        lg.info(" * The histogram bin values:")
        lg.info(self.__bins)
        lg.info(" *")

        # Set the colour of the histogram patches (make configurable?).
        #plt.setp(self.patches, 'facecolor', '#44BB11', 'alpha', 0.75, 'linewidth', 0.0)

        #print("* DEBUG: Number of hit pixels in each frame:", self.__cpf)
        #print("* DEBUG: Max number of clusters per frame  : %6d" % (self.max_x))
        #print("* DEBUG: x max                             : %6d" % (self.max_x_r))
        #print("* DEBUG: x bin width                       : %6d" % (self.bin_w))
        #print("* DEBUG: bins:", self.bins)
        #print("* DEBUG:")

        # Fit to Poisson?
        if self.__n[0] != self.__n_f: # If not completely empty...

            ## The Poisson function to fit to!
            fitfunc = lambda p, x: p[0]*pow(p[1],x)*pow(np.e,-p[1])/factorial(x)

            ## A list of the initial guess for the parameters.
            p0 = [float(self.__n_f), float(self.__Lambda_est)]

            ## The error function to perform the fitting.
            errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function

            ## The fitted parameters.
            p1 = None

            ## Did the fit succeed?
            success = None

            # Use the least square method from optimize to perform a check.
            # We won't actually use this...
            p1, success = optimize.leastsq(errfunc, p0[:], args=(self.__bins[:-1], self.__n))

            if success == 1:
                lg.info(" * FIT SUCCEEDED!")

            lg.info(" * Fitted values [Scale, \\lambda]:")
            lg.info(p1)
            lg.info(" *")

            # Use the estimated parameters from the Bayesian method.
            p_est = [float(self.__n_f), float(self.__Lambda_est)]

            # Plot the Poisson distribution from the estimated values.
            plt.bar(self.__bins, fitfunc(p_est, self.__bins), color='#CCCCCC')

            # Plot the Poisson distribution with the fitted values.
            #plt.bar(self.__bins, fitfunc(p1, self.__bins), color='#CCCCCC')

            # The expected y values from the estimated parameters.
            y_est = fitfunc(p_est, self.__bins)

            # The expected y values from the fitted parameters.
            y_fit = fitfunc(p1, self.__bins)

            # The distances from the predicted values - Bayesian estimates.
            ds_est = errfunc(p_est, self.__bins[:-1], self.__n)

            # The distances from the predicted values - fitted estimates.
            ds_fit = errfunc(p1, self.__bins[:-1], self.__n)

            for i, binval in enumerate(self.__bins[:-1]):
                lg.info(" * | % 3d | % 3d | % 3d | % 6.3f | % 10.8f | % 6.3f | % 10.8f |" %
                    (i, binval, self.__n[i], y_est[i], ds_est[i], y_fit[i], ds_fit[i]))

        # Firstly, we'll need an array of the bin centres to put the points
        # at (rather than the bin edges). Note the slicing of the bin edges
        # array to get the N bins (as otherwise we'd have N+1 bin edges).
        self.bins_centres = 0.5*(self.__bins[1:]+self.__bins[:-1])

        #lg.info(" * The bin centres:")
        #lg.info(self.bins_centres)
        #lg.info(" *")

        # Some bins will be empty. To avoid plotting these, we can replace
        # the contents of that bin with "nan" (not a number).
        # matplotlib then cleverly skips over these, leaving the x axis
        # clean and shiny.
        self.__n = [np.nan if x==0 else float(x) for x in self.__n]

        # Calculate the errors on the number of clusters counted (Poisson).
        self.__err = np.sqrt(self.__n)

        # Calculate the Chi^2 values for the estimated distribution.
        chi2_est, n_deg_est, chi2_div_est = chi2(self.__n, y_est, 1)

        lg.info(" * Estimated distribution (\hat{\Lambda}):")
        lg.info(" *--> \Chi^2      = % 7.5f" % (chi2_est))
        lg.info(" *--> N_freedom   = % d" % (n_deg_est))
        lg.info(" *")

        # Calculate the Chi^2 values for the fitted distribution.
        chi2_fit, n_deg_fit, chi2_div_fit = chi2(self.__n, y_fit, 1)
        lg.info(" * Fitted distribution:")
        lg.info(" *--> \Chi^2      = % 7.5f" % (chi2_fit))
        lg.info(" *--> N_freedom   = % d" % (n_deg_fit))
        lg.info(" *")

        # Plot the real data points as an "errorbar" plot
        plt.errorbar(self.bins_centres, \
                     self.__n, \
                     fmt='d', \
                     color='black', \
                     yerr=self.__err, \
                     ecolor='black', \
#                     capthick=2, \
                     elinewidth=1)

        # Save the figure.

        # Custom plot limits if required.
        #plt.ylim([0, 16])
        #plt.xlim([0, 20])

        self.plot.savefig(self.__output_path + "/%s.png" % (self.__name))

        self.plot.savefig(self.__output_path + "/%s.ps" % (self.__name))

        return self.__Lambda_est, self.__Lambda_est_err, chi2_est, n_deg_est
