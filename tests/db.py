from quickpos.database import Database
from quickpos.product import Product
from quickpos.transaction import Transaction
from random import shuffle, randint, choice

class Test:
  def __init__(self):
    ## Open a product api instance
    self.prod = Product()
    self.tran = Transaction()

  ## Demonstrate product input to database, and show how database is initialised
  def Product(self):
    ## Create two products
    self.prod.db.ClearTable("products")
    products = [
      ["Branstons Beans", 0.75],
      ["Hovis Bread", 1],
      ["Kinder Bueno", 0.85],
      ["Cadbury Dairy Milk", 1.5]
    ]

    ## Submit the products to database twice
    for item in range(2):
      for product in products:
        self.prod.CreateProduct(product[0], product[1])

    ## Select all from database
    instruction = """
    SELECT * FROM products
    """
    
    withduplicates = [list(i)[1:] for i in self.prod.db.ReturnRecords(instruction)]
    for item in withduplicates:
      print(item)

    ## Remove duplicates from database
    self.prod.RemoveDuplicates()
    print("Removed Duplicates")
      
    ret = self.prod.db.ReturnRecords(instruction)

    ret = [list(i) for i in ret]
    for i in ret:
      print(i)

  ## Demonstrate a transaction table based on product table
  def Transaction(self):
    ## Choose five random products, with random quantities
    products = self.prod.db.ReturnRecords("SELECT * FROM products")
    for i in range(50):
      basket = []
      for item in products:
        basket.append(choice(products))
      for item in basket:
        self.tran.RecordTransaction(item[0], randint(1,100))
    
    print("Transactions table")
    for result in self.tran.GetLedger():
      print(result)

    print("Search based on product")
    for item in self.tran.SortByProductID(choice(products)[0]):
      print(item)

if __name__ == "__main__":
  t = Test()
  t.Transaction()
