from quickpos.database import Database
from quickpos.product import Product


class Transaction:
  def __init__(self):
    self.db = Database()
    self.prod = Product()
    
  ## Record a transaction, takes a list of products and quantities as input
  def RecordTransaction(self, prodlist: list):
    rowid = self.db.LastRowID("transactions")
    for prod, quantity in prodlist:
      prod_id = prod[0]
      instruction = """
      INSERT INTO transactions (
        id,
        product_id,
        product_quantity,
        transaction_datetime
      )
      VALUES ({}, {}, {}, datetime('now', 'localtime'))
      """.format(rowid, prod_id, quantity)
      self.db.TableTransaction(instruction)

  ## Get all transactions
  def GetLedger(self):
    return self.db.ReturnRecords("SELECT * FROM transactions")
  
  ## Get information on a specific transaction
  def GetTransaction(self, transaction_id: int) -> list:
    return self.db.ReturnRecords("SELECT * FROM transactions WHERE id={}".format(transaction_id))

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

  ## Get all transactions ordered by value
  def SortByValue(self):
    instruction = """
    SELECT * FROM transactions
    ORDER BY transaction_value;
    """
    return self.db.ReturnRecords(instruction)

  ## Get the value of a given transaction
  def GetTransactionValue(self, transaction_id: int) -> float:
    value = 0
    transactions = map(lambda x: [x[1], x[2]], self.GetTransaction(transaction_id))
    for product, quantity in map(lambda x: [x[1], x[2]], self.GetTransaction(transaction_id)):
      value += self.prod.SearchForProduct(product)[2] * quantity
    return value

