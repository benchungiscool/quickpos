## Luke is a cool guy 
import sqlite3
import os


## The class to use if you need to interact with databases
## You need to pass in a filename and the instruction to create
class Database:
    ## Make sure all of the directories are in and create a table if necessary
    def __init__(self, dbName: str, tablename: str, createInstruction: str) -> None:

        ## We can use these later
        self.dbName = dbName
        self.tableName = tablename
        
        ## Check for database file
        while "main.py" not in os.listdir():
            os.chdir("..")

        ## If no database folder found, create one then change dir to it
        if "databases" not in os.listdir():
             os.mkdir("databases")
             os.chdir("databases")
        else: 
            os.chdir("databases")

        ## Call the Database Creation
        self.TableTransaction(createTable)

    ## When you want to add something to a database
    def TableTransaction(self, instruction: str) -> None:
        
        ## Establish conneciton to database
        connection = sqlite3.connect(self.dbName+".db")
        table = connection.cursor()

        ## Do the instruction
        table.execute(instruction)

        ## Save and exit
        connection.commit()
        connection.close()
    
    ## Fetch stuff from database
    def ReturnRecords(self, instruction) -> list:

        ## Establish connection to the database
        connection = sqlite3.connect(self.dbName+".db")
        table = connection.cursor()

        ## Do the instruction
        table.execute(instruction)

        ## Return the results as a list of all the results
        return table.fetchall()
    
    ## Remove the duplicates in the database
    def RemoveDuplicates(self):

        ## Get all items from a given table
        returnall = """
        SELECT *
        FROM {}
        """.format(self.tableName)

        ## Get a list of the records
        records = self.ReturnRecords(returnall)
        wasterecords = []

        ## Get a list of all the records that appear more than once
        for record in records: 
            count = records.count(record)
            if count >= 2 and record not in wasterecords:
                wasterecords.append(record)
            
        print("Wasterecords \n", wasterecords)
        
        ## Replace all duplicates with a new record
        for record in wasterecords:

            ## Remove all records of a given type from a given table
            removewasterecord = """
            DELETE FROM {}
            WHERE prid="{}"
            """.format(self.tableName, record[2])

            self.TableTransaction(removewasterecord)

            ## Add the record back once
            replacement = record
            insertreplacement = """
            INSERT INTO {}
            VALUES {}
            """.format(self.tableName, record)

            self.TableTransaction(insertreplacement)
            

## Test
"""
dbName = "items"
tableName = "products"
start = """
CREATE TABLE IF NOT EXISTS {}
(name TEXT, price INTEGER, prid TEXT)
""".format("products")

returnall = """
SELECT * 
FROM {}
""".format(tableName)

products = [
    ("Sausages", 1.50, "Saus1"),
    ("Wotsits", 0.5, "Wots1"),
    ("Bananas", 0.25, "Bana1"),
    ("Playboy Magazine", 5, "Maga1")
]

if __name__ == "__main__":  
    db = Database(dbName, tableName, start)

    for product in products:

        insertion = """
        INSERT INTO {}
        VALUES {}
        """.format(tableName, product)

        for record in range(20):
            db.TableTransaction(insertion)

    for record in db.ReturnRecords(returnall):
        print(record)
    
    print("\n")
    db.RemoveDuplicates()

    for record in db.ReturnRecords(returnall):
        print(record)
""" 
