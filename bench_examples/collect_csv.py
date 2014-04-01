import logging
from os import listdir, path

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


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
    color_list = [colormap(i) for i in np.linspace(0, 1, len(queries))]
    plt.rc('axes', color_cycle=color_list)
    labels_done = False
    for ind_subplot, store_name in enumerate(data):
        ax = plt.subplot(1, n_subplots, ind_subplot)
        # ax.set_yscale('log')
        plt.grid(True)
        df = data[store_name]
        df = df.reindex_axis(sorted(df.index), axis=0)  # sort the index (ie. nthings)
        df.dropna(how='all', inplace=True)  # delete index with no values
        if len(df.index) > 1:
            plot_lines = plt.plot(df.index, df, '-', lw=2)
            if not labels_done:
                labels_done = True
                lines += plot_lines
                labels += df.columns.values.tolist()
        else:
            plt.scatter(df.index.values.tolist() * len(df.columns), df, c=color_list, s=75)
        plt.title(store_name)
    fig.legend(lines, labels, loc='upper right')
    print('displaying figure')
    plt.show()


if __name__ == '__main__':
    dirs_graph = {1: '../bench_results/raw/selected_1graph/',
                  # 5: '../bench_results/raw/selected_5graph/',
                  10: '../bench_results/raw/selected_10graph/',
                  50: '../bench_results/raw/selected_50graph/'}

    dirs_triples = {0.5: '../bench_results/raw/one_graph_500_triples/',
                    1: '../bench_results/raw/one_graph_1k_triples/',
                    2: '../bench_results/raw/one_graph_2k_triples/',
                    4: '../bench_results/raw/one_graph_4k_triples/',
                    8: '../bench_results/raw/one_graph_8k_triples/',
                    16: '../bench_results/raw/one_graph_16k_triples/',
                    32: '../bench_results/raw/one_graph_32k_triples/',
                    64: '../bench_results/raw/one_graph_64k_triples/',
                    128: '../bench_results/raw/one_graph_128k_triples/',
                    256: '../bench_results/raw/one_graph_256k_triples/',
                    512: '../bench_results/raw/one_graph_512k_triples/',
                    1024: '../bench_results/raw/one_graph_1m_triples/'}

    dirs_forks = {0: '../bench_results/raw/one_graph_1m_triples_nofork/',
                  1: '../bench_results/raw/one_graph_1m_triples_1fork/',
                  2: '../bench_results/raw/one_graph_1m_triples_2forks/',
                  3: '../bench_results/raw/one_graph_1m_triples_3forks/',
                  4: '../bench_results/raw/one_graph_1m_triples_4forks/',
                  5: '../bench_results/raw/one_graph_1m_triples_5forks/',
                  6: '../bench_results/raw/one_graph_1m_triples_6forks/',
                  7: '../bench_results/raw/one_graph_1m_triples_7forks/',
                  8: '../bench_results/raw/one_graph_1m_triples_8forks/',
                  10: '../bench_results/raw/one_graph_1m_triples_10forks/',
                  16: '../bench_results/raw/one_graph_1m_triples_16forks/',
                  20: '../bench_results/raw/one_graph_1m_triples_20forks/'}

    dirs_seqs = {1: '../bench_results/raw/one_graph_1m_triples_1seq/',
                 2: '../bench_results/raw/one_graph_1m_triples_2seqs/',
                 5: '../bench_results/raw/one_graph_1m_triples_5seqs/',
                 10: '../bench_results/raw/one_graph_1m_triples_10seqs/',
                 20: '../bench_results/raw/one_graph_1m_triples_20seqs/'}

    dirs_sleepy_graph = {
        100: '../bench_results/raw/many_graph_32k_100graphs/',
        200: '../bench_results/raw/many_graph_32k_200graphs/',
        300: '../bench_results/raw/many_graph_32k_300graphs/',
        400: '../bench_results/raw/many_graph_32k_400graphs/',
        500: '../bench_results/raw/many_graph_32k_500graphs/',
        600: '../bench_results/raw/many_graph_32k_600graphs/',
        851: '../bench_results/raw/many_graph_32k_851graphs/',
        1000: '../bench_results/raw/many_graph_32k_1000graphs/',
    }

    means = get_means(dirs_sleepy_graph, write_csv=False)
    ndf = transform_df(means)
    display_figure(ndf)

    # NOTES: plot for forks
    # means_forks = get_means(dirs_forks, write_csv=False)
    # all_store_query_forks = transform_df(means_forks)
    # x_forks = np.array(all_store_query_forks['sleepycat'].index.tolist())
    # y_forks = np.array(all_store_query_forks['sleepycat'].values.tolist())
    # ord_forks = x_forks.argsort()
    #
    # means_seqs = get_means(dirs_seqs, write_csv=False)
    # all_store_query_seqs = transform_df(means_seqs)
    # x_seqs = np.array(all_store_query_seqs['sleepycat'].index.tolist())
    # y_seqs = np.array(all_store_query_seqs['sleepycat'].values.tolist())
    # ord_seqs = x_seqs.argsort()
    #
    # # display Sleepycat forks vs. seqs
    # plt.figure()
    # plt.plot(x_seqs[ord_seqs], y_seqs[ord_seqs], 'b', marker='o', label='sequential')
    # plt.plot(x_forks[ord_forks], y_forks[ord_forks], 'g', marker='o', label='fork')
    # plt.xlabel('number of queries')
    # plt.ylabel('time (s)')
    # plt.legend(loc='upper left')
    # plt.grid()
    # plt.show()
