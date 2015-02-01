#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Statistics functions for plotting with CERN@school.
"""

#...for the logging.
import logging as lg

#...for the MATH.
import math

def chi2(observed, expected, n_fitted_params):
    """
    Calculate the Pearson's Chi^2 value for a set of N observed and
    expected values.
    @param [in] distances List with N distances between the data and f(x_i).
    @param [in] errors List with N errors for each data point x_i.
    @param [in] n_fitted_params The number of fitted parameters in the f(x_i).
    """

    lg.info(" *")

    ## The sum of the numerator of Chi^2.
    total = 0

    ## The number of degrees of freedom.
    n_deg_free = 0

    # Find the last non-zero value in the observed data.

    ## The position of the last non-zero observed value.
    pos_non_zero = 0
    #
    for i in range(len(observed) - 1, -1, -1):
        if not math.isnan(observed[i]):
            pos_non_zero = i
            break

    lg.info(" * The last non-zero observed value is at %d" % (pos_non_zero))

    # Calculate Pearson's test statistic.
    for i in range(pos_non_zero+1):

        obs = observed[i]

        if math.isnan(obs):
            obs = 0.0

        obs = float(obs)

        exp = float(expected[i])

        dif = obs - exp

        difsq = dif**2

        val = difsq / exp

        total += val

        n_deg_free += 1

        lg.info(" * | % 3d | % 7.3f | % 7.3f | % 7.3f | % 7.3f | % 7.3f |" % (i, obs, exp, dif, difsq, val))

    lg.info(" *")

    return total, n_deg_free - n_fitted_params, total/(n_deg_free - n_fitted_params)
