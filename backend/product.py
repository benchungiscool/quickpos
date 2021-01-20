from backend.database import Database


## Product API
class Product:
  def __init__(self):
    self.db = Database()

  def CreateProduct(self, productname: str, productprice: float) -> None:

    ## Have to remove quotations, they break the insertion
    if productname and "'" in productname:
      productname = productname.replace("'", "")

    ## Check lastrowid isn't irrational
    instruction = """
    SELECT COUNT(*) FROM products;
    """
    lastrowid = int(self.db.ReturnRecords(instruction)[0][0]) + 1

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
    
    ## Remove identifiers from individual records
    results = [tuple(list(result)[1:]) for result in results]

    ## Remove duplicate items from list
    results = list(set([i for i in results]))
    
    ## Remove all items from database
    instruction = """
    DELETE FROM products
    """
    self.db.TableTransaction(instruction)

    ## Add new items to database
    for record in results:
      self.CreateProduct(record[0], record[1])

  def SearchForProduct(productname: str) -> list:
    ## Select all items with given name
    instruction = """
    SELECT * FROM products
    WHERE productname="{}"
    """.format(productname)

    ## Get all results for this search
    results = self.db.ReturnRecords(instruction)

    ## If something found, return the results
    if not results:
      return "Nothing Found"
    return results
