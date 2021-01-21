from backend.database import Database
from backend.product import Product
from random import shuffle

## Demonstrate product input to database, and show how database is initialised
class Test:
  def __init__(self):
    ## Open a product api instance
    self.prod = Product()

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

    ret = [list(i)[1:] for i in ret]
    for i in ret:
      print(i)

  def Transaction(self):
    pass

if __name__ == "__main__":
  t = Test()
  t.Product()
