## Luke is a cool guy 
import sqlite3
import os


## The class to use if you need to interact with databases
## Requires a filename, a tablename and an instruction to start
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
        self.TableTransaction(createInstruction)

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
    def RemoveDuplicates(self, columnnames: tuple) -> None:

        ## Get all items from a given table
        returnall = """
        SELECT {}
        FROM {}
        """.format(columnnames, self.tableName)

        ## Get a list of the records
        records = self.ReturnRecords(returnall)
        for item in records:
            print(item)
        wasterecords = []

        ## Get a list of all the records that appear more than once
        for record in records: 
            count = records.count(record)
            if count >= 2 and record not in wasterecords:
                wasterecords.append(record)
        
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

    def Clear(self):
        
        instruction = """
        SELECT name from sqlite_master where type="table"
        """

        ## Get all the tables in string form
        tables = self.ReturnRecords(instruction)
        tables = [str(table) for table in tables]
        
        ## Remove any remaining speech marks or brackets
        tables = [table.replace("('", "") for table in tables]
        tables = [table.replace("',)", "") for table in tables]

        for table in tables:
            print(table)
            if not "sqlite_sequence" in table:
                dropcommand = """
                DROP TABLE {}
                """.format(table)
                
                db.TableTransaction(dropcommand)

