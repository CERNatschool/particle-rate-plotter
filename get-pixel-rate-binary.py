#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 CERN@school - Getting the pixel rate binary file.

 See the README.md file for more information.

"""

# Import the code needed to manage files.
import os, glob

#...for parsing the arguments.
import argparse

#...for the logging.
import logging as lg

#...for the binary stuff.
import struct

#...for file manipulation.
from shutil import rmtree

# Import the JSON library.
import json

#...for processing the datasets.
from cernatschool.dataset import Dataset

#...for making time.
from timestuff.handlers import make_time_dir


if __name__ == "__main__":

    print("*")
    print("*==================================================*")
    print("* CERN@school - Getting the pixel rate binary file *")
    print("*==================================================*")

    # Get the datafile path from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("inputPath",       help="Path to the input dataset.")
    parser.add_argument("outputPath",      help="The path for the output files.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The path to the data file.
    datapath = args.inputPath
    #
    # Check if the output directory exists. If it doesn't, quit.
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
    lg.basicConfig(filename=os.path.join(outputpath, \
        'log_get-pixel-rate-binary.log'), filemode='w', level=level)

    lg.info(" *")
    lg.info(" * Input path          : '%s'" % (datapath))
    lg.info(" * Output path         : '%s'" % (outputpath))
    lg.info(" *")

    ## The path to the dataset.
    dataset_path = os.path.join(datapath, "RAW/ASCIIxyC")

    ## The dataset to process.
    ds = Dataset(dataset_path)

    ## The path to the geographic information JSON file.
    geo_json_path = os.path.join(datapath, "geo.json")
    #
    if not os.path.exists(geo_json_path):
        raise IOError("* ERROR: no geographics metadata JSON!")

    ## The geographic information JSON file.
    mf = open(geo_json_path, "r")
    #
    md = json.load(mf)
    mf.close()

    ## The latitude [deg.]
    lat = float(md['lat'])

    ## The longitude [deg.]
    lon = float(md['lon'])

    ## The altitude [m].
    alt = float(md['alt'])

#    ## The pixel mask.
#    mask = {}
#
#    # Extract the pixel mask from the mask file.
#    if os.path.exists(os.path.join(datapath, "mask.txt")):
#        with open(os.path.join(datapath, "mask.txt"), "r") as mask_file:
#            for l in mask_file.readlines():
#                x, y, C = l.strip().split("\t")
#                mask[int(x) + int(y)*256] = 1

    ## The frames from the dataset.
    frames = ds.getFrames((lat, lon, alt))
    #
    #frames = ds.getFrames((lat, lon, alt), pixelmask=mask)

    lg.info(" * Found %d datafiles:" % (len(frames)))

    lg.info(" *---------------------------------------------------")

    ## The chip ID.
    chip_id = frames[0].getChipId()

    # The start time of the first frame.
    run_start_time_sec = frames[0].getStartTimeSec()

    # The end time of the last frame.
    run_end_time_sec = frames[-1].getStartTimeSec()
    #
    run_end_time_sec += frames[-1].getAcqTime()

    ## The run length [s].
    run_length_sec = run_end_time_sec - run_start_time_sec

    ## The Run ID.
    run_id = "%s_%s" % (chip_id, make_time_dir(run_start_time_sec))

    lg.info(" * Chip ID          :         '%s'." % (chip_id))
    lg.info(" *")
    lg.info(" * Start time (sec) : % 15d [s]." % (run_start_time_sec))
    lg.info(" *    => '%s'" % (make_time_dir(run_start_time_sec)))
    lg.info(" * End   time (sec) : % 15d [s]." % (run_end_time_sec))
    lg.info(" *    => '%s'" % (make_time_dir(run_end_time_sec)))
    lg.info(" * Run length (sec) : % 15d [s]." % (run_length_sec))
    lg.info(" * Run length (min) : % 15.2f [min.]." % (float(run_length_sec)/60.0))
    lg.info(" *")
    lg.info(" * Run ID           : '%s'." % (run_id))
    lg.info(" *")

    ## The name of the dataset profile binary file.
    output_file_name = os.path.join(outputpath, "%s.bin" % (run_id))

    ## The binary file to write to.
    bf = open(output_file_name, "wb")

    # Loop over the frames and write the binary file.
    lg.info(" * Looping over the frames.")
    lg.info(" *")
    for i, f in enumerate(frames):

        ## The frame start time.
        sts = int(f.getStartTimeSec())

        ## The frame acquisition time.
        acq_time = int(f.getAcqTime())

        ## The number of pixels hit in the frame.
        n_p = int(f.getRawNumberOfPixels())

        lg.info(" * % 15d [s] | % 4d [s] | % 10d [pixels]" % (sts, acq_time, n_p))

        # Write the frame information to the binary file.
        bf.write(struct.pack('IhH', int(f.getStartTimeSec()), int(f.getAcqTime()), int(f.getRawNumberOfPixels())))

    # Close the binary file.
    bf.close()

    print("* Conversion complete.")
    print("* A binary file of start time, acquisition time and the")
    print("* number of hit pixels can be found in:")
    print("* '%s'" % (output_file_name))
