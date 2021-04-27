from quickpos.database import Database

## Product API
class Product:
  def __init__(self):
    self.db = Database()

  ## Creates a product with given name, price and stock
  def CreateProduct(self, name, price, stock):
    ## Ensure stock and price are both the correct datatype
    stock = int(stock)
    price = float(price)
    ## If the price is below 0, return
    if price <= 0:
      return
    ## Get primary key and add this to datasbase instruciton with name, price and stock
    lastrowid = self.db.GetLastRowID("products")
    instruction = """
    INSERT INTO products (product_id, product_name, product_price, stock)
    VALUES ({}, "{}", {}, {})
    """.format(lastrowid, name, price, stock)
    ## Send this to database
    self.db.TableTransaction(instruction)

  ## Change the stock level of a given value by a given increment
  def ChangeStockLevel(self, product, value):
    ## If stock level already exists, add this to the increment provided.
    if stock := self.GetProduct(product)[3]:
      value += stock
    ## Format instruction with product key and new value
    instruction = """
    UPDATE products
    SET stock = {}
    WHERE product_id = {}
    """.format(value, product)
    ## Send this instruction to database
    self.db.TableTransaction(instruction)
  
  ## Returns the stock level for a product
  def GetStockLevel(self, product):
    ## Format instruction with product id
    instruction = """
    SELECT stock FROM products
    WHERE product_id = {};
    """.format(product)
    ## Return item from database
    return self.db.ReturnRecords(instruction)[0][0]

  ## Remove a product from the database
  def DeleteProduct(self, product_id):
    instruction = """
    DELETE FROM products
    WHERE product_id = {};
    """.format(product_id)
    self.db.TableTransaction(instruction)

  ## Remove duplicate records from database
  def RemoveDuplicates(self):
    ## Get a unique list of products
    products = list(map(lambda x: x[1:], self.GetAllProducts()))
    products = list(dict.fromkeys(products))
    ## Clear products table
    self.db.ClearTable("products")
    ## Add the unique products to the database
    for name, price, stock in products:
      self.CreateProduct(name, price, stock)

  ## Return the record of every product
  def GetAllProducts(self):
    return self.db.ReturnRecords("SELECT * FROM products")
      
  ## Return the record of a specific product  
  def GetProduct(self, product_id):
    ## Format instruction with record for a specific product
    instruction = """
    SELECT * FROM products
    WHERE product_id = {}
    """.format(product_id)
    ## Return
    return self.db.ReturnRecords(instruction)[0]

  ## Update an existing record
  def UpdateProduct(self, product_id, product_name, product_price):
    ## Set name and price to x where product id is y
    instruction = """
    UPDATE products
    SET product_name = "{}", product_price = {}
    WHERE product_id = {}
    """.format(product_name, product_price, product_id)
    ## Send this instruction to the database
    self.db.TableTransaction(instruction)

## Main loop
