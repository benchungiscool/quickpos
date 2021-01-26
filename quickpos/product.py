from quickpos.database import Database


## Product API
class Product:
  def __init__(self):
    self.db = Database()

  def CreateProduct(self, productname: str, productprice: float) -> None:
    ## Have to remove quotations, they break the insertion
    if productname and "'" in productname:
      productname = productname.replace("'", "")

    ## Check lastrowid isn't irrational
    lastrowid = self.db.LastRowID("products") + 1

    ## Send request to database
    instruction = """
    INSERT INTO products (id, product_name, product_price)
    VALUES ({}, '{}', {})
    """.format(lastrowid, productname, productprice)
    self.db.TableTransaction(instruction)

  ## Remove the duplicates in the database
  def RemoveDuplicates(self) -> None:
    ## Get all items from a given table
    instruction = """
    SELECT *
    FROM products
    """
    results = self.db.ReturnRecords(instruction)
    
    ## Remove identifiers from individual records, remove duplicates in order
    results = list(dict.fromkeys([tuple(list(result)[1:]) for result in results]))
   
    ## Remove all items from database
    instruction = """
    DELETE FROM products
    """
    self.db.TableTransaction(instruction)

    ## Add new items to database
    for record in results:
      self.CreateProduct(record[0], record[1])

  ## Get all the products
  def GetAllProducts(self) -> list: 
    return self.db.ReturnRecords("SELECT * FROM products")

  ## Get details of a product by using its ID
  def SearchForProduct(self, product_id: int) -> list:
    ## Search for product with its ID
    instruction = """
    SELECT * FROM products
    WHERE id="{}"
    """.format(product_id)

    ## Get all results for this search
    results = self.db.ReturnRecords(instruction)

    ## We can assume IDs are unique, so just return the first item found
    if not results:
      return "Nothing Found"
    return results[0]

