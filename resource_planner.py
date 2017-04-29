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
import sys
import StringIO


def parse_args(args):
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
    parser.add_argument(
        "--freq",
        metavar="TEXT",
        help="Frequency for the plot",
        default="M",
        choices=["7d", "14d", "28d", "M", "Q"],
        )
    return vars(parser.parse_args(args))


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
        # Remove any spaces in column names
        data[sheet.lower()].rename(
            columns=lambda x: x.replace(" ", "_"),
            inplace=True)
    return data


def sort_data(data):
    """Sort data into panda dataframes.

    This function does change the two 'sorted' fields and makes them into
    individual df's.

    """
    result = {}
    sort_combos = {}
    for sheet in data:
        # Get all unique combinations of values in the sorting columns
        sort1 = data[sheet].columns[2]
        sort2 = data[sheet].columns[3]
        sort1_vals = list(pd.Series(data[sheet][sort1].unique()))
        sort2_vals = list(pd.Series(data[sheet][sort2].unique()))
        # Get a list of tuples of all possible combinations of unique
        # values in the sorting columns
        stack = []
        the_funk = {}
        for x in sort1_vals:
            for y in sort2_vals:
                stack.append((x, y))
        # Get a
        for f in stack:
            d = data[sheet]
            query_string = "{0} == '{1}' & {2} == '{3}'".format(
                sort1, f[0], sort2, f[1]
            )
            query = d.query(query_string)
            label = "{0}-{1}".format(*f)
            result[label] = query
    return result


def process_data(data, freq="M"):
    """
    Process pre-sorted dataframes to create summaries for plotting.

    """
    result = {}
    for name,df in data.items():
        # Convert strings to datetime objects
        reindexed_df = df.set_index(pd.to_datetime(df["Date"]))
        # Convert negative values to ints
        reindexed_df["Crew Available"] = pd.to_numeric(reindexed_df["Change"])
        reindexed_df.drop("Change", axis=1, inplace=True)
        # Group and sum the data, then add it to the stack to be returned
        processed_data = reindexed_df.groupby(pd.Grouper(freq=freq, label="right")).sum().cumsum().ffill()
        result[name] = processed_data
    return result


def __style_plot(g, df, **kwargs):
    """
    Apply styles and artwork to a matplotlib plot.

    """
    # Setup the chart titles
    plt.subplots_adjust(top=0.85)
    title = kwargs.get("title", None)
    if title is not None:
        g.fig.suptitle(title)
    # Set the axis labels
    g.set_axis_labels("", "Available Resources")
    # Style the axis
    for ax in g.axes.flat:
        # Style the x-axis
        for label in ax.get_xticklabels():
            label.set_rotation(75)
            label.set_fontsize(8)
        ax.xaxis.grid=True
        # Style the y-axis
        ylim = ax.get_ylim()
        ax.set_ylim(0, ylim[1]*1.1)
        ax.yaxis.set_major_locator(
            matplotlib.ticker.MaxNLocator(integer=True))
    # Plot the legend
    lgd_pln, = plt.plot(
        [], color="#4c72b0", linewidth=2, linestyle="-",
        label="Available Resources"
    )
    plt.legend(
        handles=[lgd_pln,],
        bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0
    )
    return g


def plot_data(data, fmt="png"):
    """
    Plot the data as scatter-plot charts.

    """
    result = {}
    for name, df in data.items():
        # Setup a column of str values of dates to use as labels
        df["Date"] = df.index[:].strftime("%d-%b-%Y")
        # Plot the data
        g = sns.factorplot(
            data=df,
            x="Date", y="Crew Available",
            margin_titles=False,
        )
        __style_plot(
            g, df,
            title="Test 123",
        )
        stringio = StringIO.StringIO()
        g.savefig(stringio, format=fmt)
        result[name] = stringio
    return result


def write_plots(data, fmt="png"):
    """
    Write the created plots to disk.

    """
    for name, stringio in data.items():
        stringio.seek(0)
        filename = "{0}.{1}".format(
            name.replace(" ", "-").lower(), fmt)
        with file(filename, "w") as f:
            f.write(stringio.read())


def main():
    """Main program control loop.

    Control process is as follows:

    1. Get the data

    2. Sort the data to create dataframes, then process the dataframes into
       periodical summaries

    3. Plot the data on charts and store them as StringIO buffers

    4. Write the plots to disk

    """
    args = parse_args(sys.argv[1:])
    data = get_data(args["input"])
    sorted_data = sort_data(data)
    processed_data = process_data(sorted_data, freq=args["freq"])
    plots = plot_data(processed_data)
    write_plots(plots)


if __name__ == "__main__":
    main()
