from os import listdir, path
import pandas as pd
from matplotlib import pyplot as plt


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


def df_nthings_query(means):
    # Build a dataframe for each store
    first_mean_df = means.values()[0]  # get a dataframe to have context and function names
    store_names = set(first_mean_df.columns)  # populate before we do any intersection, otherwise it's always empty
    for dataframe in means.values():
        store_names.intersection_update(dataframe.columns)

    all_store_query = {}
    # Put empty dataframes in dict with store names as keys
    for store_name in store_names:
        all_store_query[store_name] = pd.DataFrame(index=means.keys(),  # number of things
                                                   columns=first_mean_df.index.values.tolist())  # query name
    # Build each dataframe with the real values
    for n_graph, mean_df in means.items():
        for store_name in store_names:
            for func_name in mean_df.index:
                all_store_query[store_name][func_name][n_graph] = means[n_graph][store_name][func_name]

    return all_store_query


def display_figure(data):
    print('displaying figure')
    fig = plt.figure()
    n_subplots = len(data)
    lines, labels = [], []
    for ind_subplot, store_name in enumerate(data):
        ax = plt.subplot(1, n_subplots, ind_subplot)
        ax.set_xlim(min(dirs.keys()) - 1, max(dirs.keys()) + 1)
        df = data[store_name]
        plot_lines = plt.plot(df.index, df, 'o')
        if ind_subplot == 0:
            lines += plot_lines
            labels += df.columns.values.tolist()
        plt.title(store_name)
    fig.legend(lines, labels, loc='upper right')
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
    all_store_query = df_nthings_query(means)
    display_figure(all_store_query)

