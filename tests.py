#! /usr/bin/python
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

import unittest
import subprocess
import os
import StringIO
import resource_planner

FNULL = open(os.devnull, 'w')

class TestRuntime(unittest.TestCase):
    """
    Test the runtime and flow-control logic of the program.

    """

    def setUp(self):
        self.app = os.path.dirname(__file__) + "resource_planner.py"
        self.filename = "data.xlsx"
        self.wrong_filename = "data.nothere"
        self.output = "output.png"
        self.title = "Resource Title"
        self.subtitle = "Charts Subtitle"
        
    
    def test_parse_args(self):
        """
        Test the code used to parse arguments passed to the program.

        """
        # Test that it works with input file given
        result = subprocess.check_call(
            ["python", self.app, "--input", self.filename]
        )
        assert result == 0
        # Test that it accepts all args when optional args passed
        result = subprocess.check_call(
            ["python", self.app,
             "--input", self.filename,
             "--output", self.output,
             "--title", self.title,
             "--subtitle", self.subtitle,]             
        )
        assert result == 0
        # Test that it fails if no input file given
        with self.assertRaises(subprocess.CalledProcessError) as cpe:
            subprocess.check_call(
                ["python", self.app, "--input", self.wrong_filename],
                stderr=FNULL,
            )
        # Test that it fails when unknown args are passed
        with self.assertRaises(subprocess.CalledProcessError) as cpe:
            subprocess.check_call(
                ["python", self.app,
                 "--input", self.filename,
                 "--unknown", "arg"],
                stderr=FNULL,
            )
        # Test that args passed are parsed correctly
        args = [
            "--input", self.filename,
            "--output", self.output,
            "--title", self.title,
            "--subtitle", self.subtitle,
        ]
        result = resource_planner.parse_args(args)
        self.assertEqual(result.get("input"), "data.xlsx")
        self.assertEqual(result.get("output"), "output.png")
        self.assertEqual(result.get("title"), "Resource Title")
        self.assertEqual(result.get("subtitle"), "Charts Subtitle")

        
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

    
