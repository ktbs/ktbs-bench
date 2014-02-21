from rdflib import Graph


class GraphStore(Graph):
    def __init__(self, connect_args, create_func=None, create_args=[], *args, **kwargs):
        super(GraphStore, self).__init__(*args, **kwargs)
        self.connect_args = connect_args
        self.create_func = create_func
        self.create_args = create_args

    def connect(self):
        if isinstance(self.connect_args, dict):
            self.open(**self.connect_args)
        else:
            raise TypeError("connect_args must be a dict.")

    def create(self):
        if self.create_func:
            self.create_func(*self.create_args)  # TODO gerer exception si db existe deja

    def destroy(self):
        """For SQL: destroy tables of the DB, not the DB itself."""
        super(GraphStore, self).destroy(self.connect_args['configuration'])
