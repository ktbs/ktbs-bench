from rdflib import Graph


class GraphStore(Graph):
    def __init__(self, connect_args, *args, **kwargs):
        super(GraphStore, self).__init__(*args, **kwargs)
        self.connect_args = connect_args

    def connect(self):
        if isinstance(self.connect_args, list):
            self.open(*self.connect_args)
        elif isinstance(self.connect_args, dict):
            self.open(**self.connect_args)
        else:
            raise TypeError("connect_args must be either a list or a dict.")

    def create(self):
        pass
