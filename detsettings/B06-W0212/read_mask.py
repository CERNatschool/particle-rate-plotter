#!/usr/bin/env python

# Short script to count the number of masked pixels in the pixel mask.

f = open("C:/Users/twhyntie/Desktop/langton_2014-04-02/B06-W0212/detsettings/mask_bits.txt", "r")

text = f.read()

print("Number of '0's: %10d" % (text.count("0")))
print("Number of '1's: %10d" % (text.count("1")))
