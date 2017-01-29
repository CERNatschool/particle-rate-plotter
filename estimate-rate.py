#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 CERN@school - Estimate the particle rate

 See the README.md file for more information.

"""

#...for the operating system tools.
import os

#...for parsing the arguments.
import argparse

#...for the logging.
import logging as lg

#...for file manipulation.
from shutil import rmtree

# Import the JSON library.
import json

#...for the histograms.
from plotting.poisson import RateHistogram


if __name__ == "__main__":

    print("*")
    print("*=================================*")
    print("* CERN@school - estimate the rate *")
    print("*=================================*")

    # Get the datafile path from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("inputPath",       help="Path to the input dataset.")
    parser.add_argument("outputPath",      help="The path for the output files.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The path to the data file.
    datapath = args.inputPath
    #
    # Check if the input directory exists. If it doesn't, quit.
    if not os.path.isdir(datapath):
        raise IOError("* ERROR: '%s' input directory does not exist!" % (datapath))


    ## The output path.
    outputpath = args.outputPath
    #
    # Check if the output directory exists. If it doesn't, quit.
    if not os.path.isdir(outputpath):
        raise IOError("* ERROR: '%s' output directory does not exist!" % (outputpath))


    # Set the logging level.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    # Configure the logging.
    lg.basicConfig(filename=outputpath + '/log_estimate-rate.log', filemode='w', level=level)

    print("*")
    print("* Input path          : '%s'" % (datapath))
    print("* Output path         : '%s'" % (outputpath))
    print("*")


    # Set up the directories
    #------------------------

    # Create the subdirectories.

    ## The path to the frame plots.
    fppath = os.path.join(outputpath, "frameplots")
    #
    if os.path.isdir(fppath):
        rmtree(fppath)
        lg.info(" * Removing directory '%s'..." % (fppath))
    os.mkdir(fppath)
    lg.info(" * Creating directory '%s'..." % (fppath))
    lg.info("")

    ## The filename of the frame properties JSON.
    frame_properties_json_filename = os.path.join(datapath, "frames.json")
    #
    # Check if it exists. If it doesn't, quit.
    if not os.path.exists(frame_properties_json_filename):
        raise IOError("* ERROR: '%s' output directory does not exist!" \
            % (frame_properties_json_filename))

    ## The frame properties JSON file.
    ff = open(frame_properties_json_filename, "r")
    #
    fd = json.load(ff)
    ff.close()

    # The frames
    #------------

    ## The number of clusters per frame.
    ncs = []

    lg.info(" * Looping over the frames ")
    lg.info(" *-------------------------")

    # Loop over the frames.
    for f in fd:

        ## The number of clusters in the frame.
        n_k = f["n_kluster"]

        # Add to the frame property dictionaries.
        ncs.append(n_k)

        lg.info(" *--> Found % 3d clusters." % (n_k))

    ## The number of clusters plot.
    nclplot = RateHistogram(100, "ncs", fppath, True)
    ncl_Lambda, ncl_Lambda_err, ncl_chi2, ncl_n_free = nclplot.fill(ncs)

    # Make the plot display page.
    fp = ""
    fp += "<!DOCTYPE html>\n"
    fp += "<html>\n"
    fp += "  <head>\n"
    fp += "    <link rel=\"stylesheet\" type=\"text/css\" "
    fp += "href=\"assets/css/style.css\">\n"
    fp += "  </head>\n"
    fp += "  <body>\n"
    fp += "    <h1>Cluster Sorting: Frame Properties</h1>\n"
    fp += "    <h2>Dataset summary</h2>\n"
    fp += "    <p>\n"
    fp += "      <ul>\n"
    fp += "        <li>Dataset path = '%s'</li>\n" % (datapath)
    fp += "        <li>Number of frames = %d</li>\n" % (len(fd))
    fp += "      </ul>\n"
    fp += "    </p>\n"
    fp += "    <h2>Frame properties</h2>\n"
    fp += "    <table>\n"
    fp += "      <caption>Fig. 1: Clusters per frame.</caption>\n"
    fp += "      <tr><td><img src=\"ncs.png\" /></td></tr>\n"
    fp += "    </table>\n"
    fp += "    <p>Poisson distribution: &Lambda; = (% 7.3f &plusmn; % 7.3f)</p>\n" % (ncl_Lambda, ncl_Lambda_err)
    fp += "    <p>Fit to Poisson: &chi;<sup>2</sup> = % 7.3f, N<sub>f</sub> = %d.</p>\n" % (ncl_chi2, ncl_n_free)
    fp += "  </body>\n"
    fp += "</html>"

    ## The web page filename.
    framepage_filename = os.path.join(fppath, "index.html")
    #
    # Write out the frame property index page.
    with open(framepage_filename, "w") as framepage:
        framepage.write(fp)

    # Now you can view the "index.html" files to see the results!
    print("*")
    print("* Plotting complete.")
    print("* View your results by opening '%s' in a browser, e.g." % (framepage_filename))
    print("* $ firefox %s &" % (framepage_filename))
