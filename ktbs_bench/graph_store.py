from rdflib import Graph


class GraphStore(Graph):
    def __init__(self, connect_args, *args, **kwargs):
        super(GraphStore, self).__init__(*args, **kwargs)
        self.connect_args = connect_args

    def connect(self):
        self.open(*self.connect_args)
