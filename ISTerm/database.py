class Database(object):
    def __init__(self):
        self.database = []
    def put(self, storage):
        self.database.append(storage)
    def out(self):
        return self.database