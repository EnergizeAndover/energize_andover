import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd


def file_parser(file, field_to_graph='MAIN ELECTRIC METER.Analog Inputs.KW_Total.Main-kW (Trend1)',
                output_file_name='test.pdf', grouping=None):

    df = pd.read_csv(file, header=1, index_col=[0])
    if grouping is not None:
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
    graph = df[field_to_graph]
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
    plt.title(field_to_graph)
    plt.ylabel('energy in KW')
    plt.xlabel('Dates and Time')
    plt.tight_layout()
    plt.savefig(output_file_name, format='pdf')
