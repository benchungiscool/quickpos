import sqlite3
import os


## The class to use if you need to interact with databases
## Requires a filename, a tablename and an instruction to start
class Database:
  ## Make sure all of the directories are set up  and create a table if necessary
  def __init__(self) -> None:

    ## Don't need to fix this rn, problem with datetime
    transactionInstruction = """ 
    CREATE TABLE IF NOT EXISTS transactions (
      id INTEGER NOT NULL,
      product_id INTEGER NOT NULL,
      product_quantity INTEGER NOT NULL,
      transaction_value REAL NOT NULL,
      transaction_date datetime('yyyy-MM-dd HH:mm')
    );
    """
    createInstruction = [
    """
    CREATE TABLE IF NOT EXISTS products (
      id INTEGER,
      product_name TEXT NOT NULL,
      product_price REAL NOT NULL
    );
    """,
    ]

    ## Check for database file
    while "main.py" not in os.listdir():
      os.chdir("..")

    ## If no database folder found, create one then change dir to it
    if "databases" not in os.listdir():
      os.mkdir("databases")
    os.chdir("databases")

    ## Set up filename and open a cursor
    self.dbName = "transactions.db"
    self.table = self.OpenCursor()
    
    ## Call the Database Creation for each table
    for instruction in createInstruction:
      self.TableTransaction(instruction)

  ## Returns a cursor object, helpful in later functions
  def OpenCursor(self):
    self.connection = sqlite3.connect(self.dbName)
    return self.connection.cursor()
    
  ## When you want to add something to a database
  def TableTransaction(self, instruction: str) -> None:
    ## Do the instruction
    self.table.execute(instruction)
    self.connection.commit()

  ## Fetch stuff from database
  def ReturnRecords(self, instruction) -> list:
    ## Do the instruction
    self.table.execute(instruction)

    ## Return the results as a list of all the results
    return self.table.fetchall()

  def Clear(self):
    instruction = """
    SELECT name from sqlite_master where type="table"
    """

    ## Get all the tables in string form
    tables = [str(table).strip("('").strip("'),") for table in self.ReturnRecords(instruction)]

    for table in tables:
      if not "sqlite_sequence" in table:
        dropcommand = """
        DROP TABLE {}
        """.format(table)
          
        self.TableTransaction(dropcommand)

