import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd


def file_parser(file,
                field_to_graph='',
                output_file_name='test.pdf',
                grouping='min',
                total=False,
                ):
    graph_error = False
    df = pd.read_csv(file, header=1, index_col=[0])
    if total:
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
            df = df.groupby(df.index, sort=True).max() - df.groupby(df.index, sort=True).min()
    else:
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
            df = df.groupby(df.index, sort=True).sum()
    if df.columns.__contains__(field_to_graph):
        graph = df[field_to_graph]
    else:
        graph = df[df.columns[0]]
        graph_error = True
    if len(graph.index) > 20:
        graph.plot.bar(grid=True,
                       use_index=True,
                       figsize=(len(graph.index) / 4, 20)
                       )
    else:
        graph.plot.bar(grid=True,
                       use_index=True,
                       figsize=(10, 10)
                       )
    plt.xticks(rotation='vertical')
    if graph.name == field_to_graph:
        plt.title(graph.name)
    else:
        plt.title(field_to_graph +
                  ' not found first column graphed\n' +
                  graph.name)
    plt.ylabel(graph.name)
    plt.xlabel('Dates and Time')
    plt.tight_layout()
    plt.savefig(output_file_name, format='pdf')
    plt.cla()
    plt.clf()
    return graph_error
