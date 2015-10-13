CERN@school Particle Rate Plotter
=================================

This code is for estimating the mean rate of particles
detected with CERN@school Timepix detectors.

For full instructions, see the wiki on the right.

* `process-frames.py`: processes Pixelman frames (Pixelman format)
into frame images, as well as producing a JSON of the frame
properties;
* `estimate-rate.py`: estimates the particle rate (assuming the
particle detection rate follows a Poisson distribution);
* `get-pixel-rate-binary.py`: produces a compressed binary file
of the frame start times, acquisition times, and number of hit
pixels for super-speedy data scoping;
* `profile-data-by-day.py`: uses the binary scoping file to
produce an hour-by-hour plot of a specified day in the data set
(so you will need to know which day you want to look at).

To run the unit tests, use:

```bash
$ nose2
```

##To Do

* Reformat the geographical information JSON information;
* Add pixel mask functionality;
* Rename the data and DSC files with chip ID and start time info?
* Add unit tests for the `plotting` directory;
* Add unit tests for the `visualisation` directory;
* Add unit tests for the `timestuff` directory;
* Streamline things a bit...

##Useful links

* [CERN@school homepage](http://cernatschool.web.cern.ch).
