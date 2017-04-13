#! /usr/bin/python
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

import unittest
import os
import StringIO
import resource_planner
import pandas as pd
from StringIO import StringIO
from contextlib import contextmanager

FNULL = open(os.devnull, 'w')


@contextmanager
def capture_sys_output():
    """
    Capture stdout and stderr to avoid printing messages to the CLI.
    """
    capture_out, capture_err = StringIO(), StringIO()
    current_out, current_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = capture_out, capture_err
        yield capture_out, capture_err
    finally:
        sys.stdout, sys.stderr = current_out, current_err

        
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
        # Test that it fails if no input file given
        args = []
        with self.assertRaises(AttributeError) as context:
            with capture_sys_output as (stdout, stderr):
                resource_planner.parse_args(args)
        self.assertEqual(str(context.exception), "__exit__")
        # Test that it fails when unknown args are passed
        args = [
            "--input", self.filename,
            "--unknown", "arg"
        ]
        with self.assertRaises(AttributeError) as context:
            with capture_sys_output as (stdout, stderr):
                resource_planner.parse_args(args)
        self.assertEqual(str(context.exception), "__exit__")
        # Test that it works with only the input file given
        args = ["--input", self.filename]
        result = resource_planner.parse_args(args)
        self.assertEqual(len(result), 4)
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
        self.xlsx_file = os.path.dirname(__file__) + "data.xlsx"
        self.xlsx_wrongfile = os.path.dirname(__file__) + "not.here"
        self.cols = [ "Date", "Change", "Sort_1", "Sort_2" ]
        planning = pd.DataFrame(                  
            data=[
                [ "2017-01-01", "10", "Red", "Jellybeans", ],
                [ "2017-01-01", "20", "Green", "Jellybeans", ],
                [ "2017-01-01", "25", "Green", "Frogs", ],
                [ "2017-01-01", "15", "Red", "Frogs" ],
                [ "2017-02-01", "-10", "Red", "Frogs" ],
            ],
            columns=["Date", "Change", "Sort_1", "Sort_2"],
            )
        others = pd.DataFrame(data={"Date": [], "Change": [],
                                    "Sort 1": [], "Sort 2": []})
        self.data = {
            "planning": planning,
            "leave": others,
            "required": others,
            "margin": others,
        }

        
    def test_get_data(self):
        """
        Test the code used to get and parse the Excel data.

        Note:

          This test suite relies on the included "data.xlsx" file to provide
          assurance that the data is being read into the correct format.

          Removing or modifying this example file may cause this test to fail.

        """
        # Check that an IOError is raised if the file cannot be found
        with self.assertRaises(IOError) as context:
            resource_planner.get_data(self.xlsx_wrongfile)
        # Check that the sample input data can be parsed from the xlsx file
        result = resource_planner.get_data(self.xlsx_file)
        # 4 pages in the workbook, so 4 df's
        self.assertEqual(len(result), 4) 
        # Check 5 columns in each sheet
        for sheet in result:
            self.assertEqual(len(result[sheet].columns), 5)


    def __compare_df_values(self, df1, df2):
        """
        Compare 2 df's to see if they have the same values.

        """
        matrix = df1.values == df2.values
        if False in matrix:
            return False
        else:
            return True
        
            
    def test_process_data(self):
        """
        Test the code used to process the raw data into a Pandas df.

        """
        result = resource_planner.sort_data(self.data)
        # Check that sample data is returned correctly
        expected = pd.DataFrame(
            data=[["2017-01-01", "10", "Red", "Jellybeans"],],
            columns=self.cols[0:4],
        )
        self.assertTrue(
            self.__compare_df_values(result["Red-Jellybeans"], expected))
        expected = pd.DataFrame(
            data=[["2017-01-01", "20", "Green", "Jellybeans"],],
            columns=self.cols[0:4],
            index=[0,]
        )
        self.assertTrue(
            self.__compare_df_values(result["Green-Jellybeans"], expected))
        expected = pd.DataFrame(
            data=[["2017-01-01", "25", "Green", "Frogs"],],
            columns=self.cols[0:4],
        )
        self.assertTrue(
            self.__compare_df_values(result["Green-Frogs"], expected))
        expected = pd.DataFrame(
            data=[["2017-01-01", "15", "Red", "Frogs"],
                  ["2017-02-01", "-10", "Red", "Frogs"],],
            columns=self.cols[0:4],
        )
        self.assertTrue(
            self.__compare_df_values(result["Red-Frogs"], expected))



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

    
