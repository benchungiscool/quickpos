import database


## Implement the reusability of the more widely used queries in this project
## Also implement some customisability with tablenames etc, so mulitple databases
## with similar attributes are possible
class Queries:
    ## Set tablename as an attribute of the class
    def __init__(self, tablename: str):
        self.tablename = tablename

    ## Request that creates a product library
    def ProductTable(self):
        request = """
        CREATE TABLE IF NOT EXISTS {} (
        [prid] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        [name] TEXT NOT NULL,
        [price] INTEGER NOT NULL);
        """.format(self.tablename)
        return request

    def ReturnAll(self):
        request = """
        SELECT * FROM {}
        """.format(self.tablename)
        return request

    
