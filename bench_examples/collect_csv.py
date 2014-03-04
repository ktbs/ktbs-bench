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


if __name__ == '__main__':
    dirs = {1: '../bench_results/raw/selected_1graph/',
            5: '../bench_results/raw/selected_5graph/',
            10: '../bench_results/raw/selected_10graph/'}

    means = {k: None for k in dirs.keys()}

    # Get the means for all runs
    for n_graph, checkup_dir in dirs.items():
        files = get_files(checkup_dir, '.csv')
        csv_dir = path.dirname(checkup_dir)
        abs_files = map(lambda f: path.join(csv_dir, f), files)  # list of csv files with absolute paths

        big_df = concat_data(abs_files)
        mean = big_df.groupby(big_df.index).mean()
        means[n_graph] = mean
        mean.to_csv(path.join(csv_dir, 'mean.csv'))  # outputs mean

        big_df.groupby(big_df.index).std().to_csv(path.join(csv_dir, 'std.csv'))  # outputs standard deviation

    # Build a dataframe per store
    first_mean_df = means.values()[0]
    store_names = set(first_mean_df.columns)  # populate before we do any intersection, otherwise it's always empty
    for dataframe in means.values():
        store_names.intersection_update(dataframe.columns)

    all_store_query = {}
    # Put empty dataframes in dict with store names as keys
    for store_name in store_names:
        all_store_query[store_name] = pd.DataFrame(index=means.keys(),
                                                   columns=first_mean_df.index.values.tolist())
    # Build each dataframe with the real values
    for n_graph, mean_df in means.items():
        for store_name in store_names:
            for func_name in mean_df.index:
                all_store_query[store_name][func_name][n_graph] = means[n_graph][store_name][func_name]

    # Display all the figures
    print('displaying figure')
    fig = plt.figure()
    n_subplots = len(all_store_query)
    lines, labels = [], []
    for ind_subplot, store_name in enumerate(all_store_query):
        ax = plt.subplot(1, n_subplots, ind_subplot)
        ax.set_xlim(min(dirs.keys()) - 1, max(dirs.keys()) + 1)
        df = all_store_query[store_name]
        plot_lines = plt.plot(df.index, df, 'o')
        if ind_subplot == 0:
            lines += plot_lines
            labels += df.columns.values.tolist()
        plt.title(store_name)
    fig.legend(lines, labels, loc='upper right')
    plt.show()
