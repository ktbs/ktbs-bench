from sys import argv

from os import listdir, path
import pandas as pd


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
    checkup_dir = argv[1]
    files = get_files(checkup_dir, '.csv')
    csv_dir = path.dirname(checkup_dir)
    abs_files = map(lambda f: path.join(csv_dir, f), files)  # List of csv files with absolute paths

    big_df = concat_data(abs_files)
    big_df.groupby(big_df.index).mean().to_csv(path.join(csv_dir, 'mean.csv'))  # Output mean
    big_df.groupby(big_df.index).std().to_csv(path.join(csv_dir, 'std.csv'))  # Output standard deviation
