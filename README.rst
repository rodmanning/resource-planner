==================
 Resource Planner
==================

:AUTHOR: Rod Manning <rod.manning@taslytic.com>
:ORGANIZATION: Taslytic Solutions Pty Ltd	 
:COPYRIGHT: Taslytic Solutions (c) 2017
:VERSION: 0.0
:DATE: 07-04-2017	  
:ABSTRACT:
   Python program for determining the number of resources available given
   changes on particular dates

 
What This Software Does
=======================

This software computes the number of resources available on a given date. It
plots this as a chart showing the number of resources available over a
specified period of time.

It is designed to be used to help organisations plan recruitment and training
programs to maintain the desired number of staff.

It also plots minimum and maximum resource lines to represent the upper- and
lower limits of the expected resources due to changes such as annual leave,
recruitment and resignations.

How It Does This
================

The program takes a MS Excel file as an input. This spreadsheet has 3 sheets:

======== =======================================================================
Sheet    Details 
======== =======================================================================
Planned  The planned number of staff available.

         - The first row represents the number of staff available at the start.

	 - Subsequent rows show change to number of staff on a particular date.
-------- -----------------------------------------------------------------------
Required The number of staff required.

         - The first row represents the number of staff available at the start.

	 - Subsequent rows show change to number of staff on a particular date.
-------- -----------------------------------------------------------------------
Leave    The change to crew numbers when staff commence, and return, from
         annual leave on particular dates.

	 - All rows show changes from the baselines already included in the
	   *Planned* sheet.
-------- -----------------------------------------------------------------------
Margin   How much margin is allowed for above the *minimum* line.

         - The first row represents how much margin should be allowed for at the
	   start of the period.

	 - Subsequent rows show change to margin on a particular date.
======== =======================================================================

Installation
============

Source Code
-----------

The source code is availbale from:

  https://github.com/rodmanning/resource-planner

Installation
------------

1. Download the source code from the respository noted above

2. Ensure the following dependcies are installed:

   - Python 2.x
   - Pandas
   - Seaborn
   - wxPython (GUI)
   - Gooey (GUI)

3. Run the program either using the GUI or from the CLI

License
=======

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file, You
can obtain one at http://mozilla.org/MPL/2.0/.
