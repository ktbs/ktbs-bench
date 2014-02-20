from csv import DictWriter

from ktbs_bench.utils.decorators import bench


@bench
def batch_insert(graph, file):
    """Insert triples in batch."""
    print(graph, file)


if __name__ == '__main__':
    # Define some graph/store to use
    graph_list = ['g1', 'g2']

    # Define some files to get the triples from
    n3file_list = ['f1', 'f2']

    # Testing batch insert
    res = {'func_name': 'batch_insert'}
    for graph in graph_list:
        for n3file in n3file_list:
            time_res = batch_insert(graph, n3file)
            res[time_res[0]] = time_res[1]

    # Setup the result CSV
    with open('/tmp/res.csv', 'wb') as outfile:
        res_csv = DictWriter(outfile, fieldnames=res.keys())
        res_csv.writeheader()

        # Write the results
        res_csv.writerow(res)
