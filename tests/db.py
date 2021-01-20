from backend.database import Database
from backend.product import Product

## Demonstrate product input to database, and show how database is initialised
class Test:
  def __init__(self):
    ## Open a product api instance
    self.prod = Product()

  def Product(self):
    ## Create two products
    products = [
      ["Branston's Beans", 0.75],
      ["Hovis Bread", 1]
    ]
  
    ## Submit the products to database twice
    for product in products:
      self.prod.CreateProduct(product[0], product[1])

    ## Select all from database
    instruction = """
    SELECT * FROM products
    """

    for item in self.prod.db.ReturnRecords(instruction):
      print(item)

    ## Remove duplicates from database
    self.prod.RemoveDuplicates()
      
    ## Check database has removed duplicates
    for item in self.prod.db.ReturnRecords(instruction):
      print(item)

  def Transaction(self):
    pass

if __name__ == "__main__":
  t = Test()
  t.Product()
