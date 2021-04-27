from quickpos.product import Product
from quickpos.database import Database


class Transaction:
  def __init__(self):
    self.db = Database()
    self.prod = Product()

  ## Record a transaction using a list of products
  def RecordTransaction(self, *args):
    ## Get the primary key
    lastrowid = self.GetOrderID()
    ## For each product in products list provided as parameter
    for product, product_quantity in args:
      ## Update stock levels
      self.prod.ChangeStockLevel(product, -product_quantity)
      ## Format instruction with primary key, product and quantity
      instruction = """
      INSERT INTO transactions (id, product, product_quantity, transaction_datetime)
      VALUES ({}, {}, ABS({}), datetime('now', 'localtime'));
      """.format(lastrowid, product, product_quantity)
      ## Send instruction to database
      self.db.TableTransaction(instruction)

  ## Get OrderID for the transaction table
  def GetOrderID(self):
    ## Select highest OrderID from transaction table
    instruction = """
    SELECT MAX(id) FROM transactions;
    """
    ## If nothing returned from this request, make orderid 0
    if not (lastorderid := self.db.ReturnRecords(instruction)[0][0]):
      lastorderid = 0
    ## Increment by one, then return
    return lastorderid + 1

  ## Get all products and quantities from a given day
  def GetProductsByDate(self, date):
    ## Get all transactions from a day
    records = list(filter(lambda x: date in x[3], self.GetAllTransactions()))
    ## Return the products and quantities from this
    return list(map(lambda x: [x[1], x[2]], records))

  def AverageSales(self, product):
    ## Get Transactions
    transactions = self.GetAllTransactions()
    ## Get unique dates from transactions
    days = list(dict.fromkeys(list(map(lambda x: x[3].split(" ")[0], transactions))))
    ## If there are no days, return 0
    if not len(days):
      return 0
    ## Get total product sold 
    totalsales = []
    for day in days:
      ## Get transactions with target product in
      daytransactions = list(filter(lambda x: x[0] == product, self.GetProductsByDate(day)))
      ## Add together the quantities of the target product in a day
      daytransactions = sum(list(map(lambda x: x[1], daytransactions)))
      totalsales.append(daytransactions)
    ## Return the total sales divided by the number of days
    return sum(totalsales) / len(days)

  def DaysProductLeft(self, product):
    ## Get average stock levels for product
    averagesales = self.AverageSales(product)
    ## Get stock level
    stocklevel = self.prod.GetStockLevel(product)
    ## If no data for either value, return 0
    if not averagesales or not stocklevel:
      return 0
    ## Round down the two items divided by one another to get the days
    return int(stocklevel / averagesales)

  ## Return all of the transactions in the database
  def GetAllTransactions(self):
    return self.db.ReturnRecords("SELECT * FROM transactions")

  ## Get a specific transaction
  def GetTransaction(self, transaction_id):
    instruction = """
    SELECT * FROM transactions
    WHERE id = {};
    """.format(transaction_id)
    return self.db.ReturnRecords(instruction)
  
## Remove a transaction from the transactions table
  def RemoveTransaction(self, transaction_id):
    ## Delete from the transactions table, where id is the given number
    instruction = """
    DELETE FROM transactions
    WHERE id = {}
    """.format(transaction_id)
    ## Send this to the database
    self.db.TableTransaction(instruction)


## Main loop
