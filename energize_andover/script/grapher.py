import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd


def file_parser(file,
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
    for field in field_to_graph:
        if df.columns.__contains__(field):
            graph[field] = df[field]
        else:
            graph[df.columns[0]] = df[df.columns[0]]
            graph_error = True
    if len(graph.index) > 20:
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
                           figsize=(10, 10)
                           )
        elif graph_type == 'barh':
            graph.plot.barh(grid=True,
                            use_index=True,
                            figsize=(10, 10)
                            )
        elif graph_type == 'line':
            graph.plot.line(grid=True,
                            use_index=True,
                            figsize=(10, 10)
                            )
        elif graph_type == 'area':
            graph.plot.area(grid=True,
                            use_index=True,
                            figsize=(10, 10)
                            )
        else:
            graph.plot.bar(grid=True,
                           use_index=True,
                           figsize=(10, 10)
                           )
    plt.xticks(rotation='vertical')
    plt.title(title)
    plt.ylabel(units)
    plt.xlabel('Dates and Time')
    plt.tight_layout()
    plt.savefig(output_file_name, format='pdf')
    plt.cla()
    plt.clf()
    return graph_error
