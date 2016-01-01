import argparse
import pandas as pd
import numpy as np
from datetime import timedelta
import re


def parse(input_file):
    """Parse a file generated by the Metasys application

    Args:
        input_file: string, indicating path of Metasys file

    Returns:
        pandas DataFrame, with timestamps as index and measurement variables as columns
    """
    # Read the file into a pandas Series with MultiIndex
    df = pd.read_csv(input_file, index_col=[0, 1])['Object Value']

    # Remove units from values, so that they are numeric
    df = df.apply(drop_units)

    # Transform df from 1-dimensional Series with MultiIndex to 2-dimensional DataFrame
    df = df.unstack(level=-1)

    # Remove prefixes from column names
    df.columns = [drop_prefix(column_name) for column_name in df.columns]

    # Convert index to DatetimeIndex
    df.index = pd.to_datetime(df.index, dayfirst=True)

    return df


def drop_prefix(variable_name):
    """Remove the 'Town Of Andover:AHS-NAE1/FEC Bus2.' prefix from variable names"""
    pattern = re.compile(r"\ATown Of Andover:AHS-NAE1/FEC Bus2\.(.*)\Z")
    match = pattern.match(variable_name)
    if match is None:
        # variable_name was not of the expected format
        return np.nan
    else:
        return match.group(1)


def drop_units(value):
    """Remove the units from a string, e.g. '309.2 kWh' -> 309.2"""
    pattern = re.compile(r"\A(\d*\.?\d+) [a-zA-Z]+\Z")
    match = pattern.match(value)
    if match is None:
        # value was not of the expected format
        return np.nan
    else:
        return float(match.group(1))


def summarize(df, start_time=None, end_time=None):
    """Return a table describing daily energy usage"""
    if (start_time is None) != (end_time is None):
        raise ValueError('start_time and end_time should both be either present or not present')
    elif start_time is not None and end_time is not None:
        df = df.iloc[df.index.indexer_between_time(start_time, end_time),:]

    grouped = df.groupby(df.index.shift(-1, freq=timedelta(hours=12)).date)

    grouped_cumulative_energy = grouped[[
        'MAIN ELECTRIC METER.Analog Inputs.Energy.Main-kWh-Energy (Trend1)',
        'PANEL DHB ELECTRIC METER.Analog Inputs.Energy.DHB - kWh Total (Trend1)',
        'PANEL M1 ELECTRIC METER.Analog Inputs.Energy.M1-kWh-Energy (Trend1)',
        'PANEL DG ELECTRIC METER.Analog Inputs.Energy.DG-kWh-Energy (Trend1)',
        'PANEL DE-ATS ELECTRIC METER.Analog Inputs.Energy.DE-ATS-Energy-kWh (Trend1)',
        'PANEL COLLINS ELECTRIC METER.Analog Inputs.Energy.CollinCtr-Energy-kWh (Trend1)',
        'PANEL DL ELECTRIC METER.Analog Inputs.Energy.DL-Energy-kWh (Trend1)'
    ]]
    daily_energy = grouped_cumulative_energy.max() - grouped_cumulative_energy.min()
    daily_energy.columns = [['Main', 'DHB', 'M1', 'DG', 'DE-ATS', 'Collins', 'DL']]

    return daily_energy


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='script for parsing Metasys data files')
    parser.add_argument('-s', '--summarize', dest='summarize', action='store_true',
                        help='option indicating whether output file should be a summary')
    parser.add_argument('--start', dest='start_time', nargs='?',
                        help='start time for summary table')
    parser.add_argument('--end', dest='end_time', nargs='?', help='end time for summary table')
    parser.add_argument('-i', dest='input_file',  help='name of input file')
    parser.add_argument('-o', dest='output_file', help='name of output file')
    args = parser.parse_args()
    transformed = parse(args.input_file)
    if args.summarize:
        transformed = summarize(transformed, args.start_time, args.end_time)
    transformed.to_csv(args.output_file)
