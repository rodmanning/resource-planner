#! /usr/bin/python
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

import unittest


class TestRuntime(unittest.TestCase):
    """
    Test the runtime and flow-control logic of the program.

    """

    def setUp(self):
        pass
    
    
    def test_parse_args(self):
        """
        Test the code used to parse arguments passed to the program.

        """
        pass


class TestData(unittest.TestCase):
    """
    Test the data reading, parsing, and outputs of the app.

    """

    
    def setUp(self):
        pass


    def test_get_date(self):
        """
        Test the code used to get and parse the Excel data.

        """
        pass

    
    def test_process_data(self):
        """
        Test the code used to process the raw data into a Pandas df.

        """
        pass


class TestPlotting(unittest.TestCase):
    """
    Test the code used to create plots and write them to disk.

    """

    
    def setUp(self):
        pass
    
    
    def test_plot_data(self):
        """
        Test the code used to plot the charts using Seaborn.

        """
        pass


    def test_write_plots(self):
        """
        Test the code used to write the charts to disk.

        """
        pass

    
