import sqlite3
import os


## The class to use if you need to interact with databases
## Requires a filename, a tablename and an instruction to start
class Database:
  ## Make sure all of the directories are set up  and create a table if necessary
  def __init__(self) -> None:

    ## Set up filename
    self.dbName = "transactions.db"

    createInstruction = [
    """
    CREATE TABLE IF NOT EXISTS products (
      product_id INTEGER,
      product_name TEXT NOT NULL,
      product_price REAL NOT NULL,
      PRIMARY KEY (product_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS transactions (
      transaction_id INTEGER PRIMARY KEY,
      products_id INTEGER NOT NULL,
      product_quantity INTEGER NOT NULL,
      transaction_value REAL NOT NULL,
      FOREIGN KEY(products_id) REFERENCES products(product_id)
    );
    """
    ]

    ## Check for database file
    while "main.py" not in os.listdir():
      os.chdir("..")

    ## If no database folder found, create one then change dir to it
    if "databases" not in os.listdir():
      os.mkdir("databases")
      os.chdir("databases")
    else: 
      os.chdir("databases")
    
    ## Call the Database Creation for each table
    for instruction in createInstruction:
      self.TableTransaction(instruction)

  def GetCurrentID(self, tablename: str):
    instruction = """
    SELECT MAX({}) FROM {}
    """.format(str(tablename[:-1])+"_id", tablename)

    results = self.TableTransaction(instruction)
    
    if not results:
      results = 0
    return results + 1

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
          
        db.TableTransaction(dropcommand)

