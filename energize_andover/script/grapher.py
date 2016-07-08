import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

'''
    file_grapher: creates and saves a graph based on data in a given csv file.
    inputs:
            file(String): path to input data file
            field_to_graph(List of strings): list of column headers of the data to graph
            output_file_name(string): path to the output file
            grouping(string): string that represents the time grouping of the data.
            total(boolean): makes the graph either the difference or average between the start and end time groupings.
            title(String): title of the graph
            units(String): Y- axis label of the graph
            graph_type(String): type of graph
    output:
            graph_error(boolean): indicates if there was an error when graphing or not.
'''
def file_grapher(file,
                field_to_graph=[''],
                output_file_name='test.pdf',
                grouping='min',
                total=False,
                title='',
                units='',
                graph_type='bar'
                ):
    graph_error = False
    graph = pd.DataFrame()
    df = pd.read_csv(file, header=1, index_col=[0])
    df = df.replace(0, np.NaN) # modify data to condier 0 as empty data
    # change index based on groupings
    if not grouping == 'min':
        index = df.index
        new_index = []
        if grouping == 'month':
            for date in index:
                new_index.append(date[:7])
        elif grouping == 'day':
            for date in index:
                new_index.append(date[:10])
        elif grouping == 'hour':
            for date in index:
                new_index.append(date[:13])
        df.index = new_index
        # change data to difference or average based on total
        if total:
            df = df.groupby(df.index, sort=True).max() - df.groupby(df.index, sort=True).min()
        else:
            df = df.groupby(df.index, sort=True).mean()
    # create a data frame to graph based on the strings in fields_to_graph
    for field in field_to_graph:
        if df.columns.__contains__(field):
            graph[field] = df[field]
        # set data to first column if not in data and indicate error
        else:
            graph[df.columns[0]] = df[df.columns[0]]
            graph_error = True
    # add day of the week to index
    new_index = []
    for time in graph.index:
        new_index.append(add_weekday(time))
    graph.index = new_index
    # create plot based on graph_type and the amount of data
    if len(graph.index) > 80:
        if graph_type == 'bar':
            graph.plot.bar(grid=True,
                           use_index=True,
                           figsize=(len(graph.index) / 4, 20)
                           )
        elif graph_type == 'barh':
            graph.plot.barh(grid=True,
                            use_index=True,
                            figsize=(20, len(graph.index) / 4)
                            )
        elif graph_type == 'line':
            graph.plot.line(grid=True,
                            use_index=True,
                            figsize=(len(graph.index) / 4, 20)
                            )
        elif graph_type == 'area':
            graph.plot.area(grid=True,
                            use_index=True,
                            figsize=(len(graph.index) / 4, 20)
                            )
        else:
            graph.plot.bar(grid=True,
                           use_index=True,
                           figsize=(len(graph.index) / 4, 20)
                           )
    else:
        if graph_type == 'bar':
            graph.plot.bar(grid=True,
                           use_index=True,
                           figsize=(20, 10)
                           )
        elif graph_type == 'barh':
            graph.plot.barh(grid=True,
                            use_index=True,
                            figsize=(10, 20)
                            )
        elif graph_type == 'line':
            graph.plot.line(grid=True,
                            use_index=True,
                            figsize=(20, 10)
                            )
        elif graph_type == 'area':
            graph.plot.area(grid=True,
                            use_index=True,
                            figsize=(20, 10)
                            )
        else:
            graph.plot.bar(grid=True,
                           use_index=True,
                           figsize=(20, 10)
                           )
    # improve graphs aesthetics
    plt.xticks(rotation='vertical')
    plt.title(title)
    plt.ylabel(units)
    plt.xlabel('Dates and Time')
    plt.tight_layout()
    plt.savefig(output_file_name, format='pdf')
    plt.cla()
    plt.clf()
    return graph_error

'''
    add_weekday: adds the day of the week to date time string
    Inputs:
            date(string): date time string to be edited
    Output:
            (String) date time string with day of the week
'''
def add_weekday(date):
    if len(date) > 13:
        dt = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%Y-%m-%d %H:%M %a')
    elif len(date) > 10:
        dt = datetime.strptime(date, '%Y-%m-%d %H')
        return dt.strftime('%Y-%m-%d %H:00 %a')
    elif len(date) > 7:
        dt = datetime.strptime(date, '%Y-%m-%d')
        return dt.strftime('%Y-%m-%d %a')
    else:
        return date