#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

CERN@school: Data Profiling - HTML page tools.

See http://cernatschool.web.cern.ch for more information.

"""

#...for the time (being).
import time

#...for handling the time strings.
from handlers import getPixelmanTimeString

def make_css():
    """ Add the web page CSS - see The Woork Handbook (A. Lupetti). """

    ## The CSS string to return.
    s = '''
/* ----------------------- */
/* STANDARD HTML TAG RESET */
/* ----------------------- */
  body,
  h1, h2, h3,
  p, ul, li,
  form {
    border:0;
    margin:0px;
    padding:0px;
  }

/* ---------------------------- */
/* STANDARD HTML TAG DEFINITION */

  body, form, input {
    color:#000000;
    font-family:Arial, Helvetica, sans-serif;
    font-size:12px;
    color:#000000;
  }

  h1{font-size:24px;}

  h2{font-size:18px;}

  h3{font-size:13px;}

  a:link, a:visited{
    color:#0033CC;
  }

  table{
    color: #222222;
    border-collapse: collapse;
    border-spacing: 0;
    margin: 20px;
    width: 90%;
  }

  td, th {
    border: 1px solid #cccccc;
    /* height: 30px; */
    transition: all 0.3s;
    padding: 5px;
  }

  th {
    background: #e2e2e2;
    font-weight: bold;
  }

  td{
    background: #f5f5f5;
    font-family: Monospace;
  }

  td.number {
    text-align:right;
  }

  tr:nth-child(even) td {
    background: #f5f5f5;
  }

  tr:nth-child(odd) td {
    background: #fcfcfc;
  }

  tr td:hover {
    background: #778877;
    color: #ffffff;
  }

/* ----------------------------*/
/* PAGE ELEMENTS               */
/* ----------------------------*/
  #container{
    margin: 30px auto;
    width:100%;
  }

/* ---------------------------*/
/* FOOTER                     */
  #footer{
    clear:both;
    color:#666666;
    font-size:11px;
    text-align:center;
  }

/* ---------------------------*/
/* CUSTOM                     */
  .caption {
    font-family:Arial, Helvetica, sans-serif;
    text-align:center;
  }
'''

    return s


def make_day_plot_page(plot_names):

    """
    Make a plot profile page for a given day.

    @param [in] plot_names Dictionary of plot names { hour:path }.
    """

    ## The string to return for the page.
    s = '''<!DOCTYPE html>
<html>
<head>
  <!-- <link rel="stylesheet" type="text/css" href="main.css"> -->
  <style>
{{CSS}}
  </style>
</head>
<div id="container">

  <!-- Main Content -->
  <div id="main">
    <table>

{{TABLE_ROWS}}
    </table>
  </div>

  <!-- Footer -->
  <div id="footer">&copy; CERN@school 2015</div>

</div>
</html>
'''

    ## The table contents (generated from the supplied dictionary).
    t = "      "

    # Loop over the plots.
    for i, hour in enumerate(sorted(plot_names.keys())):

        t += "    <tr>"

        # Add the image tag to the table.
        t += "<td class=\"number\">%02d</td><td><img style=\"width: 100%%\" src=\"%s\" /></td>" % (int(hour), plot_names[hour])

    t += "</tr>\n"

    # Add the table contents.
    s = s.replace('{{TABLE_ROWS}}', t)

    # Add the CSS inline to the web page.
    s = s.replace('{{CSS}}', make_css())

    return s
