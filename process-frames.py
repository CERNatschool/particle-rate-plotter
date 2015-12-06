#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 CERN@school - Processing Frames

 See the README.md file and the GitHub wiki for more information.

 http://cernatschool.web.cern.ch

"""

#...for the operating stuff.
import os

#...for the file processing.
import glob

#...for parsing the arguments.
import argparse

#...for the logging.
import logging as lg

#...for file manipulation.
from shutil import rmtree

# Import the JSON library.
import json

#...for processing the datasets.
from cernatschool.dataset import Dataset

#...for making time.
from cernatschool.handlers import make_time_dir

#...for making the frame and clusters images.
from visualisation.visualisation import makeFrameImage


if __name__ == "__main__":

    print("*")
    print("*======================================*")
    print("* CERN@school - local frame processing *")
    print("*======================================*")

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

    # Check if the output directory exists. If it doesn't, quit.
    if not os.path.isdir(outputpath):
        raise IOError("* ERROR: '%s' output directory does not exist!" % (outputpath))

    # Set the logging level.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    # Configure the logging.
    lg.basicConfig(filename = outputpath + '/log_process-frames.log', filemode='w', level=level)

    print("*")
    print("* Input path          : '%s'" % (datapath))
    print("* Output path         : '%s'" % (outputpath))
    print("*")

    # Set up the directories
    #------------------------

    # Create the subdirectories.

    ## The path to the frame images.
    frame_output_path = os.path.join(outputpath, "PNG")
    #
    if os.path.isdir(frame_output_path):
        rmtree(frame_output_path)
        lg.info(" * Removing directory '%s'..." % (frame_output_path))
    os.mkdir(frame_output_path)
    lg.info(" * Creating directory '%s'..." % (frame_output_path))
    lg.info("")

    ## The path to the dataset.
    dataset_path = os.path.join(datapath, "RAW/ASCIIxyC")

    ## The dataset to process.
    ds = Dataset(dataset_path)

    # Get the metadata from the JSON.

    ## The frame metadata.
    fmd = None
    #
    with open(os.path.join(datapath, "geo.json"), "r") as fmdf:
        fmd = json.load(fmdf, fmd)
    #
    ## Latitude of the dataset [deg.].
    lat = fmd['lat'] # [deg.]
    #
    ## Longitude of the dataset [deg.].
    lon = fmd['lon'] # [deg.]
    #
    ## Altitude of the dataset [m].
    alt = fmd['alt'] # [m]

    ## The pixel mask.
    pixel_mask = {}

    with open(os.path.join(datapath, "masked_pixels.txt"), "r") as mpf:
        rows = mpf.readlines()
        for row in rows:
            vals = [int(val) for val in row.strip().split("\t")]
            x = vals[0]; y = vals[1]; X = (256*y) + x; C = 1
            pixel_mask[X] = C

    ## The frames from the dataset.
    frames = ds.getFrames((lat, lon, alt), pixelmask = pixel_mask)

    lg.info("* Found %d datafiles." % (len(frames)))

    ## A list of frames.
    mds = []

    # Loop over the frames and upload them to the DFC.
    for f in frames:

        ## The basename for the data frame, based on frame information.
        bn = "%s_%s" % (f.getChipId(), make_time_dir(f.getStartTimeSec()))

        #bn = "%s_%d-%06d" % (f.getChipId(), f.getStartTimeSec(), f.getStartTimeSubSec())

        # Create the frame image.
        makeFrameImage(bn, f.getPixelMap(), frame_output_path, f.getPixelMask())

        # Create the metadata dictionary for the frame.
        metadata = {
            "id"          : bn,
            #
            "chipid"      : f.getChipId(),
            "hv"          : f.getBiasVoltage(),
            "ikrum"       : f.getIKrum(),
            #
            "lat"         : f.getLatitude(),
            "lon"         : f.getLongitude(),
            "alt"         : f.getAltitude(),
            #
            "start_time"  : f.getStartTimeSec(),
            "end_time"    : f.getEndTimeSec(),
            "acqtime"     : f.getAcqTime(),
            #
            "n_pixel"     : f.getNumberOfUnmaskedPixels(),
            "occ"         : f.getOccupancy(),
            "occ_pc"      : f.getOccupancyPc(),
            #
            "n_kluster"   : f.getNumberOfKlusters(),
            "n_gamma"     : f.getNumberOfGammas(),
            "n_non_gamma" : f.getNumberOfNonGammas(),
            #
            "ismc"        : int(f.isMC())
            }

        # Add the frame metadata to the list of frames.
        mds.append(metadata)

    # Write out the frame information to a JSON file.
    # We will use this later to make the frame plots,
    # rather than processing the whole frame set again.
    #
    with open(os.path.join(outputpath, "frames.json"), "w") as jf:
        json.dump(mds, jf)
