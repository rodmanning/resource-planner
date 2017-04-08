#! /usr/bin/python
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import argparse


def parse_args():
    """
    Parse arguments passed to the program.
    """
    parser = argparse.ArgumentParser(
        description="Resource Planner to determine number of resources available",
        epilog="Copyright (c) Taslytic Solutions. Licensed under the MPL v2.0",
        add_help=True,        
       )
    parser.add_argument(
        "--input",
        metavar="FILE",
        help="The input file (xlsx-format)",
        default="data.xlsx",
        required=True,
        )
    parser.add_argument(
        "--output",
        metavar="FILE",
        help="The output file for the charts",
        default="output.png"
        )
    parser.add_argument(
        "--title",
        metavar="TEXT",
        help="Title for the plot",
        default="Resource Plot"
        )
    parser.add_argument(
        "--subtitle",
        metavar="TEXT",
        help="Sub-title for the plot (optional)",
        default=None,
        )
    args = parser.parse_args()
    return vars(args)


def get_data(path):
    """
    Get data for the program from an input xlsx file.

    path: 
      The path to the MS Excel (xlsx) file used as input.
    """
    data = {}
    excel_file = pd.ExcelFile(path)
    for sheet in excel_file.sheet_names:
        data[sheet.lower()] = excel_file.parse(sheet)
    return data

def process_data():
    """
    Process data into panda dataframes.
    """
    pass


def plot_data():
    """
    Plot the data as scatter-plot charts.
    """
    pass


def write_plots():
    """
    Write the created plots to disk.
    """
    pass


def main():
    """
    Main program control loop.
    """
    args = parse_args()
    data = get_data(args["input"])
    
if __name__ == "__main__":
    main()
