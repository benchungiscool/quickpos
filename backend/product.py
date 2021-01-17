from backend.database import Database


## Product API
class Product:
  def __init__(self):
    self.db = Database()

  def CreateProduct(self, productname: str, productprice: float) -> None:

    ## Have to remove quotations, they break the insertion
    productname = productname.replace("'", "")

    ## Send request to database
    instruction = """
    INSERT INTO products (product_id, product_name, product_price)
    VALUES ({}'{}', {})
    """.format(str(self.db.GetCurrentID("products")) + ", ", productname, productprice)

    self.db.TableTransaction(instruction)

  ## Remove the duplicates in the database
  def RemoveDuplicates(self, tablename: str) -> None:

    ## Get all items from a given table
    instruction = """
    SELECT *
    FROM {}
    """.format(tablename)
    results = self.db.ReturnRecords(instruction)
    
    ## Remove identifier, we don't need it
    results = results[1:]

    results = list(dict.fromkeys(results[1:]))
    
    ## Remove all items from database
    instruction = """
    DELETE FROM {}
    """.format(tablename)
    self.db.TableTransaction(instruction)

    ## Add new items to database
    for record in results:
      self.CreateProduct(record[0], record[1])

  def SearchForProduct(productname: str) -> list:
    instruction = """
    SELECT * FROM products
    WHERE productname="{}"
    """.format(productname)

    results = self.db.ReturnRecords(instruction)

    return results

 
if __name__ == "__main__": 
  products = [
  ["Branston's Beans", 0.75],
  ["Hovis Bread", 1]
  ]

  prod = Product()
  for product in products:
    for i in range(2):
      prod.CreateProduct(product[0], product[1])

  instruction = """
  SELECT * FROM products
  """
  for item in prod.db.ReturnRecords(instruction):
    print(item)

  prod.RemoveDuplicates("products")

