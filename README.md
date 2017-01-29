# CERN@school: Particle Rate Plotter
This code is for estimating the mean rate of particles
detected with a
[Timepix detector](http://medipix.web.cern.ch)
using the method described in Section 3 of the CERN@school
**Contemporary Physics** paper
([Whyntie et al. 2015](http://dx.doi.org/10.1080/00107514.2015.1045193))
and the CERN@school "how-to" guide on
[FigShare](https://dx.doi.org/10.6084/m9.figshare.895961.v1).
There is also code for plotting the time profile (i.e. the number
of pixels detected over a time series) for a given dataset for a
given day).
The datasets featured in the paper are included with the code,
but may also be found on [FigShare](http://figshare.org)
[here](https://dx.doi.org/10.6084/m9.figshare.1618851.v2).

## Overview
This `README.md` file has become rather large, so here's an overview:
* **Some disclaimers**;
* **Getting the code**: how to get the code and set up your system;
* **Processing the frames**: turn the raw detector data into useful cluster information;
* **Plotting the cluster frequency**: plot the clusters-per-frame histogram and fit to a Poisson distribution;
* **Plotting the time profile**: plot the number of pixels per unit time over the course of a day;
* **Unit tests**: how to check everything (well, almost everything) is working;
* **The sample datasets**: some information about the datasets featured in this work;
* **Acknowledgements**;
* **Useful links**. 


## Some disclaimers
* _This code dates from 2015. While every attempt has been
made to ensure that it is usable, some work may be required to get it
running on your own particular system.
We recommend using a GridPP CernVM; please refer to
[this guide](http://doi.org/10.6084/m9.figshare.4552825.v1)
for further instructions.
Unfortunately CERN@school cannot guarantee further support for this code.
Please proceed at your own risk_.
* _This repository is now deprecated, and remains here for legacy purposes.
For future work regarding CERN@school, please refer to the
[Institute for Research in Schools](http://researchinschools.org) (IRIS)
[GitHub repository](https://github.com/InstituteForResearchInSchools).
Please also feel free to fork and modify this code as required for
your own research._


## Getting the code
To get the code, create a working directory on your CernVM and
clone it from GitHub with the following command:

```bash
$ git clone https://github.com/CERNatschool/particle-rate-plotter.git
$ cd particle-rate-plotter
```

To prepare for running, run the `setup.sh` script with the following
command:

```bash
$ source setup.sh
```

_Note: if you are not using a GridPP CernVM, the `setup.sh` script
will not work as you won't have access to the CERN@school CVMFS
repository and will have to source your own version of the Python
libraries such as `matplotlib` via e.g. the
[Anaconda Python distribution](http://anaconda.org)._


## Processing the frames
The first thing to do is process the raw data from the detector
into images and clusters that we can analyse further.
The `process-frames.py` Python script processes the frames
into frame images, as well as producing a JSON of the frame
properties.
For the MX-10 data set (chip ID `B06-W0212`), we process the frames
with the following commands:

```bash
$ mkdir ../tmp-mx10/
$ python process-frames.py ./testdata/B06-W0212/2014-04-02-150255/ ../tmp-mx10/
*
*======================================*
* CERN@school - local frame processing *
*======================================*
*
* Input path          : 'testdata/B06-W0212/2014-04-02-150255/'
* Output path         : '../tmp-mx10/'
*
```

The directory `../tmp-mx10` should now be full of results, which you can check with
the following command:

```bash
$ ls ../tmp-mx10
PNG  frames.json  log_process-frames.log
```

The code has extracted the properties of the data frames
into the `frames.json` JSON file
(more on [JSON files here](http://www.w3schools.com/json/)) - so we
don't have to run the processing code again - and created image files
of all the frames and the clusters.
You can view the frames any standard image viewer.
On the GridPP CernVM, for example, you can use the Eye of Gnome viewer:

```bash
$ sudo yum install eog
[... say 'yes' to everything and type your password when asked ...]
$ eog ../tmp-mx10/frames/ &
```

You can then view each image by pressing the left or right arrow keys.


## Plotting the cluster frequency
Having processed the frames and extracted the frame and cluster
information, we can now perform some analysis on our data.
The first thing we can do is plot a frequency histogram of the
number of clusters detected per frame.
Furthermore, as explained in
([Whyntie et al. 2015](http://dx.doi.org/10.1080/00107514.2015.1045193)),
by fitting a Poisson distribution to this frequency histogram,
we can estimate the mean rate of particles detected per unit time - which
can give us a handle on the background radiation level where we made
the measurement.

The following command will perform the analysis and produce the plot:

```bash
$ python estimate-rate.py ../tmp-mx10/ ../tmp-mx10/
*
*=================================*
* CERN@school - estimate the rate *
*=================================*
*
* Input path          : '../tmp-mx10/'
* Output path         : '../tmp-mx10/'
*
* Plotting complete.
* View your results by opening '../tmp-mx10/frameplots/index.html' in a web browser, e.g.
* $ firefox ../tmp-mx10/frameplots/index.html &
```

You can view the plot - as displayed in a webpage with
accompanying statistical information - by using the command:

```bash
$ firefox ../tmp-mx10/frameplots/index.html &
```

This is figure 3 a) of
([Whyntie et al. 2015](http://dx.doi.org/10.1080/00107514.2015.1045193)).
To produce figure 3 b), i.e. the corresponding plot for the Mk1 detector's
dataset, we need to run the commands again, specifying a _different output
directory_, with the Mk1 dataset:

```bash
$ mkdir ../tmp-mk1/
$ python process-frames.py ./testdata/E09-W0092/2014-04-02-150315/ ../tmp-mk1/
[... output ...]
$ python estimate-rate.py ../tmp-mk1/ ../tmp-mk1/
[... output ...]
$ firefox ../tmp-mk1/frameplots/index.html & 
```


## Plotting the time profile
To plot the time profiles of a given dataset, we need two scripts.
The first,
 `get-pixel-rate-binary.py`,
produces a binary file
of the frame start times, acquisition times, and number of hit
pixels for super-speedy data scoping - i.e. we don't have to read in
the raw data each time.
The `profile-data-by-day.py` Python script then uses this binary
scoping file to produce an hour-by-hour plot of a specified day in the 
data set (so you will need to know which day you want to look at).

### Converting the data to a binary file
First, let's convert the datasets into two binary files of the frame
start times, acquisition times, and number of hit pixels in each
frame with the following command:

```bash
$ python get-pixel-rate-binary.py testdata/B06-W0212/2014-04-02-150255/ ../tmp-mx10/
*
*==================================================*
* CERN@school - Getting the pixel rate binary file *
*==================================================*
* Conversion complete.
* A binary file of start time, acquisition time and the
* number of hit pixels can be found in:
* '../tmp-mx10/B06-W0212_2014-04-02-140255.bin'
$ python get-pixel-rate-binary.py testdata/E09-W0092/2014-04-02-150315/ ../tmp-mk1/
[... similar output ...]
```


### Making the time profile

We can then make the plots of the hit pixels per second
across the twenty-four hours of the day with the
following commands:

```bash
$ python profile-data-by-day.py ../tmp-mx10/B06-W0212_2014-04-02-140255.bin ../tmp-mx10/ 2014-04-02-UTC -1 0
[...output...]
* Profile plots made for Wed Apr  2 00:00:00 2014.
* These can be viewed with the following command:
* $ firefox ../tmp-mx10/2014-04-02-UTC/pixel-profile.html &
```

To get the same plots for the Mk1 dataset, use:
```bash
$ python get-pixel-rate-binary.py testdata/E09-W0092/2014-04-02-150315/ ../tmp-mk1/
[... corresponding output ...]
$ firefox ../tmp-mk1/2014-04-02-UTC/pixel-profile.html &
```

Note that this is just the number of pixels per frame - not
the number of clusters. There may be many pixels in a single cluster.

_**Exercise**: can you make a different version of the script that makes
a time profile of the number of clusters detected per unit time?_


## The unit tests

Testing code to make sure it's running as expected is always a
good idea. We've provided code to run some **unit tests** on some
of the Python objects used in the scripts here.
If you have `nose` installed, you cam run these unit tests with:

```bash
$ nose2
....
----------------------------------------------------------------------
Ran 4 tests in 0.887s

OK
```

_To install `nose2` on your GridPP CernVM, type:_

```bash
$ sudo pip install nose2
```

_and enter your password when requested._


## The sample datasets
The data featured in this repository were recorded with a
CERN@school MX-10 particle camera (chip ID `B06-W0212`) and a
CERN@school Mk1 detector (chip ID `E09-W0092`).
Please see
([Whyntie et al. 2015](http://dx.doi.org/10.1080/00107514.2015.1045193))
for more details of the experimental methods used.
You may also find the datasets in the
[FigShare](http://figshare.org) repository
[here](https://dx.doi.org/10.6084/m9.figshare.1618851.v2).


## Acknowledgements
CERN@school was supported by
the UK [Science and Technology Facilities Council](http://www.stfc.ac.uk) (STFC)
via grant numbers ST/J000256/1 and ST/N00101X/1,
as well as a Special Award from the Royal Commission for the Exhibition of 1851.


## Useful links
* [Setting up a GridPP CernVM](http://doi.org/10.6084/m9.figshare.4552825.v1);
* [Whyntie et al. 2015](http://dx.doi.org/10.1080/00107514.2015.1045193) - the CERN@school Contemporary Physics paper featuring this experiment (Section 3);
* The [sample datasets](https://dx.doi.org/10.6084/m9.figshare.1618851.v2) as featured in (Whyntie et al. 2015);
* The [Institute for Research in Schools](http://researchinschools.org) (IRIS) homepage;
* The [IRIS CERN@school website](http://researchinschools.org/CERN);
* The [Official IRIS GitHub Organization](https://github.com/InstituteForResearchInSchools).
