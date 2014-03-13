import logging

from os import listdir, path
import pandas as pd
from matplotlib import pyplot as plt
from numpy import linspace

logging.getLogger(__name__)


def get_files(directory, file_extension):
    """Get a list of filenames with a specific extension."""
    return filter(lambda f: f.endswith(file_extension), listdir(directory))


def concat_data(file_list):
    """Take multiple csv files and merge the tables in one big table."""
    df_list = []
    for file in file_list:
        with open(file, 'r') as f:
            df_list.append(pd.read_csv(f, index_col='func_name'))
    return pd.concat(df_list)


def get_means(dirs, write_csv=True):
    """Return the means for each directory that contain several time measures.

    :param dict dirs: directories to look into, {number_of_things : path}
    :param bool write_csv: True to output mean and std in CSV files, False otherwise
    :returns means: means for each thing
    :rtype: dict
    """
    means = {k: None for k in dirs.keys()}

    # Get the means for all runs
    for n_graph, checkup_dir in dirs.items():
        files = get_files(checkup_dir, '.csv')
        csv_dir = path.dirname(checkup_dir)
        abs_files = map(lambda f: path.join(csv_dir, f), files)  # list of csv files with absolute paths

        # Put all the results in a DataFrame
        big_df = concat_data(abs_files)
        # Compute the mean
        mean = big_df.groupby(big_df.index).mean()
        means[n_graph] = mean

        if write_csv:
            mean.to_csv(path.join(csv_dir, 'mean.csv'))  # outputs mean
            big_df.groupby(big_df.index).std().to_csv(path.join(csv_dir, 'std.csv'))  # outputs standard deviation

    return means


def transform_df(means):
    """Change representation of dataframes.

    Means is a dictionnary with nthings as keys, and DataFrame as values.
    Each DataFrame as store name for columns and query for index.
    This function transforms to a dictionnary with store name as keys,
    DataFrame as values. Where DataFrame columns are query and index are nthings.

    :param dict means: dataframes with store name / query for each nthings
    :return: dataframes with query / nthings for each store name
    :rtype: dict
    """
    # Build a dataframe for each store
    first_mean_df = means.values()[0]  # get a dataframe to have context and function names
    store_names = set(first_mean_df.columns)  # populate before we do any intersection, otherwise it's always empty

    all_store_query = {}
    # Put empty dataframes in dict with store names as keys
    for store_name in store_names:
        all_store_query[store_name] = pd.DataFrame(index=means.keys(),  # number of things
                                                   columns=first_mean_df.index.values.tolist())  # query name
    # Build each dataframe with the real values
    for n_graph, mean_df in means.items():
        for store_name in store_names:
            for func_name in mean_df.index:
                try:
                    all_store_query[store_name][func_name][n_graph] = means[n_graph][store_name][func_name]
                except KeyError, e:
                    logging.warning("Cannot put this value in the dataframe: %s" % e)

    return all_store_query


def display_figure(data):
    """Plot query times as function of nthings for each store.

    Data must be a dictionnary with store names as keys and dataframes as values.
    Dataframes must have query names as columns and nthings as index.

    :param dict data: well formatted data
    """
    fig = plt.figure()
    n_subplots = len(data)
    lines, labels = [], []
    colormap = plt.get_cmap('Set1')
    queries = data.values()[0].columns
    color_list = [colormap(i) for i in linspace(0, 1, len(queries))]
    plt.rc('axes', color_cycle=color_list)
    for ind_subplot, store_name in enumerate(data):
        ax = plt.subplot(1, n_subplots, ind_subplot)
        ax.set_xlim(min(dirs.keys()) - 1, max(dirs.keys()) + 1)
        # ax.set_yscale('log')
        plt.grid(True)
        df = data[store_name]
        df = df.reindex_axis(sorted(df.index), axis=0)  # sort the index (ie. nthings)
        plot_lines = plt.plot(df.index, df, '-', lw=2)
        if ind_subplot == 0:
            lines += plot_lines
            labels += df.columns.values.tolist()
        plt.title(store_name)
    fig.legend(lines, labels, loc='upper right')
    print('displaying figure')
    plt.show()


if __name__ == '__main__':
    dirs_graph = {1: '../bench_results/raw/selected_1graph/',
                  5: '../bench_results/raw/selected_5graph/',
                  10: '../bench_results/raw/selected_10graph/',
                  50: '../bench_results/raw/selected_50graph/', }

    dirs_triples = {32000: '../bench_results/raw/many_graph_32000/',
                    256000: '../bench_results/raw/many_graph_256000/',
                    1000000: '../bench_results/raw/many_graph_1M/'}

    dirs = dirs_triples
    means = get_means(dirs, write_csv=False)
    all_store_query = transform_df(means)
    display_figure(all_store_query)
