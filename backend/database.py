## Luke is a cool guy 
import sqlite3
import os


class Database:
    def __init__(self, dbName: str, tableName: str):

        self.dbName = dbName
        self.tableName = tableName
        
        ## Check for database file
        while "main.py" not in os.listdir():
            os.chdir("..")

        ## If no database folder found, create one then change dir to it
        if "databases" not in os.listdir():
             os.mkdir("databases")
             os.chdir("databases")

        
        
        instruction = """
        CREATE TABLE IF NOT EXISTS {}
        (name, price, productid)
        """.format(tableName)


    def TableTransaction(self, connection):
        connection = sqlite3.connect(dbName+".db")
        table = connection.cursor()

        table.execute(instruction)

        connection.close()


        
db = Database("items", "items")
