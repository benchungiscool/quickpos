import sqlite3
import os

class Database:
  def __init__(self):
    ## Navigate to parent directory
    while "quickpos" not in os.listdir():
      os.chdir("..")

    ## Navigate to databases folder
    if "databases" not in os.listdir():
      os.mkdir("databases")
    os.chdir("databases")

    ## Open cursor
    self.table = self.OpenCursor()

    ## Create database table 
    createInstruction = [
      """
      CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        product_price REAL NOT NULL,
        stock INTEGER
      );
      """,
      """
      CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER NOT NULL,
        product INTEGER,
        product_quantity INTEGER,
        transaction_datetime DATETIME,
        FOREIGN KEY(product) REFERENCES products(product_id)
      );
      """
    ]

    ## Send creation instructions to database
    for instruction in createInstruction:
      self.TableTransaction(instruction)

  ## Creates a database connection and returns a dataabase cursor
  def OpenCursor(self):
    ## Open Connection
    self.connection = sqlite3.connect("database.db")
    ## Return Cursor
    return self.connection.cursor()

  ## Send instruction to the database
  def TableTransaction(self, instruction):
    ## Send instruciton to database
    self.table.execute(instruction)
    ## Save changes
    self.connection.commit()

  ## Retrieve records from the database
  def ReturnRecords(self, instruction):
    ## Send instruction to database
    self.table.execute(instruction)
    ## Return results
    return self.table.fetchall()

  ## Get the last primary key in table
  def GetLastRowID(self, table):
    ## Select the last primary key from table
    instruction = """
    SELECT COUNT(*) FROM {};
    """.format(table)
    ## Return the result, incremented by 1
    return self.ReturnRecords(instruction)[0][0] + 1

  ## Clear a database table
  def ClearTable(self, tablename):
    ## Delete everything from a database table
    instruction = """
    DELETE FROM {}
    """.format(tablename)
    ## Send instruction to database
    self.TableTransaction(instruction)

## Main loop
if __name__ == "__main__":
  d = Database()
  instruction = """
  ALTER TABLE products
  ADD COLUMN stock;
  """
  d.TableTransaction(instruction)

