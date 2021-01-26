from quickpos.database import Database
from quickpos.product import Product


class Transaction:
  def __init__(self):
    self.db = Database()
    
  def RecordTransaction(self, prod_id: int, quantity: int):
    ## Get some information about the product
    rowid = self.db.LastRowID("transactions")
    instruction = "SELECT * FROM transactions WHERE product_id={}".format(prod_id)
    price = self.db.ReturnRecords(instruction)

    ## Add this data to an instruction template
    instruction = """
    INSERT INTO transactions (
      id,
      product_id,
      product_quantity,
      transaction_datetime
    )
    VALUES ({}, {}, {}, datetime('now', 'localtime'))
    """.format(rowid, prod_id, quantity, price, quantity*price)
    print(instruction)

    ## Submit instruction to database
    self.db.TableTransaction(instruction)

  ## Get all items
  def GetLedger(self):
    return self.db.ReturnRecords("SELECT * FROM transactions")

  ## Find an item by product id
  def SortByProductID(self, product_id: int) -> list:
    instruction = """
    SELECT * FROM transactions
    WHERE product_id={}
    """.format(product_id)
    return self.db.ReturnRecords(instruction)
  
  ## Sort either by date range or a single date
  def SortByDate(self, furthestdate: str, closestdate=None) -> list:
    if furthestdate and closestdate:
      instruction = """
      SELECT * FROM transactions
      WHERE transaction_date BETWEEN {} AND {}
      ORDER BY transaction_date;
      """.format(furthestdate, closestdate)
    else:
      instruction = """
      SELECT * FROM transactions 
      WHERE transaction_date={}
      ORDER BY transaction_date;
      """.format(furthestdate)
    return self.db.ReturnRecords(instruction)

  def SortByValue(self):
    instruction = """
    SELECT * FROM transactions
    ORDER BY transaction_value;
    """
    return self.db.ReturnRecords(instruction)

  def GetTransactionValue(self, transaction_id: int) -> float:
    prod = Product()
    value = 0
    for i in self.SortByProductID(transaction_id):
      print(i[1])
      value += prod.SearchForProduct(i[1])[0][2]
    return value

