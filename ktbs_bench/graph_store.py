from rdflib import Graph


class GraphStore(Graph):
    def __init__(self, open_args, *args, **kwargs):
        super(GraphStore, self).__init__(*args, **kwargs)
        self.open_args = open_args

    def connect(self):
        self.open(*self.open_args)
