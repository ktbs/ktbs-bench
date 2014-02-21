from rdflib import Graph


class GraphStore(Graph):
    def __init__(self, connect_args, create_func=None, *args, **kwargs):
        super(GraphStore, self).__init__(*args, **kwargs)
        self.connect_args = connect_args
        self.create_func = create_func

    def connect(self):
        if isinstance(self.connect_args, list):
            self.open(*self.connect_args)
        elif isinstance(self.connect_args, dict):
            self.open(**self.connect_args)
        else:
            raise TypeError("connect_args must be either a list or a dict.")

    def create(self):
        if self.create_func:
            self.create_func()
