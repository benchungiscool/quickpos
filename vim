diff --git a/.gitignore b/.gitignore
index 2b163cd..ebaaec2 100644
--- a/.gitignore
+++ b/.gitignore
@@ -1,2 +1,8 @@
 *.db
-__pycache__
\ No newline at end of file
+.DS_Store
+__pycache__
+*.swo
+*.swp
+venv
+databases
+flasktest
diff --git a/backend/database.py b/backend/database.py
deleted file mode 100644
index 299b44e..0000000
--- a/backend/database.py
+++ /dev/null
@@ -1,89 +0,0 @@
-import sqlite3
-import os
-
-
-## The class to use if you need to interact with databases
-## Requires a filename, a tablename and an instruction to start
-class Database:
-  ## Make sure all of the directories are set up  and create a table if necessary
-  def __init__(self):
-    createInstruction = [
-    """
-    CREATE TABLE IF NOT EXISTS products (
-      id INTEGER,
-      product_name TEXT NOT NULL,
-      product_price REAL NOT NULL
-    );
-    """,
-    """ 
-    CREATE TABLE IF NOT EXISTS transactions (
-      id INTEGER NOT NULL,
-      product_id INTEGER NOT NULL,
-      product_quantity INTEGER NOT NULL,
-      transaction_datetime datetime
-    );
-    """
-    ]
-
-    ## Check for database file
-    while "main.py" not in os.listdir():
-      os.chdir("..")
-
-    ## If no database folder found, create one then change dir to it
-    if "databases" not in os.listdir():
-      os.mkdir("databases")
-    os.chdir("databases")
-
-    ## Set up filename and open a cursor
-    self.dbName = "transactions.db"
-    self.table = self.OpenCursor()
-    
-    ## Call the Database Creation for each table
-    for instruction in createInstruction:
-      self.TableTransaction(instruction)
-
-  ## Returns a cursor object, helpful in later functions
-  def OpenCursor(self):
-    self.connection = sqlite3.connect(self.dbName)
-    return self.connection.cursor()
-
-  def LastRowID(self, tablename: str) -> int:
-    instruction = """
-    SELECT COUNT(*) FROM {};
-    """.format(tablename)
-    return self.ReturnRecords(instruction)[0][0]
-    
-  ## When you want to add something to a database
-  def TableTransaction(self, instruction: str):
-    ## Do the instruction
-    self.table.execute(instruction)
-    self.connection.commit()
-
-  ## Fetch stuff from database
-  def ReturnRecords(self, instruction) -> list:
-    self.table.execute(instruction)
-    return self.table.fetchall()
-
-  ## Remove all data from a table
-  def ClearTable(self, tablename: str):
-    instruction = """
-    DELETE FROM {}
-    """.format(tablename)
-
-  ## Removes all database tables from a file 
-  def ClearFile(self):
-    instruction = """
-    SELECT name from sqlite_master where type="table"
-    """
-
-    ## Get all the tables in string form
-    tables = [str(table).strip("('").strip("'),") for table in self.ReturnRecords(instruction)]
-
-    for table in tables:
-      if not "sqlite_sequence" in table:
-        dropcommand = """
-        DROP TABLE {}
-        """.format(table)
-          
-        self.TableTransaction(dropcommand)
-
diff --git a/backend/product.py b/backend/product.py
deleted file mode 100644
index d4c0b26..0000000
--- a/backend/product.py
+++ /dev/null
@@ -1,61 +0,0 @@
-from backend.database import Database
-
-
-## Product API
-class Product:
-  def __init__(self):
-    self.db = Database()
-
-  def CreateProduct(self, productname: str, productprice: float) -> None:
-
-    ## Have to remove quotations, they break the insertion
-    if productname and "'" in productname:
-      productname = productname.replace("'", "")
-
-    ## Check lastrowid isn't irrational
-    lastrowid = self.db.LastRowID("products") + 1
-
-    ## Send request to database
-    instruction = """
-    INSERT INTO products (id, product_name, product_price)
-    VALUES ({}, '{}', {})
-    """.format(lastrowid, productname, productprice)
-    self.db.TableTransaction(instruction)
-
-  ## Remove the duplicates in the database
-  def RemoveDuplicates(self) -> None:
-
-    ## Get all items from a given table
-    instruction = """
-    SELECT *
-    FROM products
-    """
-    results = self.db.ReturnRecords(instruction)
-    
-    ## Remove identifiers from individual records, remove duplicates in order
-    results = list(dict.fromkeys([tuple(list(result)[1:]) for result in results]))
-   
-    ## Remove all items from database
-    instruction = """
-    DELETE FROM products
-    """
-    self.db.TableTransaction(instruction)
-
-    ## Add new items to database
-    for record in results:
-      self.CreateProduct(record[0], record[1])
-
-  def SearchForProduct(productname: str) -> list:
-    ## Select all items with given name
-    instruction = """
-    SELECT * FROM products
-    WHERE productname="{}"
-    """.format(productname)
-
-    ## Get all results for this search
-    results = self.db.ReturnRecords(instruction)
-
-    ## If something found, return the results
-    if not results:
-      return "Nothing Found"
-    return results
diff --git a/backend/transaction.py b/backend/transaction.py
deleted file mode 100644
index 2593d0d..0000000
--- a/backend/transaction.py
+++ /dev/null
@@ -1,61 +0,0 @@
-from backend.database import Database
-
-
-class Transaction:
-  def __init__(self):
-    self.db = Database()
-    
-  def RecordTransaction(self, prod_id: int, quantity: int):
-    ## Get some information about the product
-    rowid = self.db.LastRowID("transactions")
-    instruction = "SELECT * FROM transactions WHERE product_id={}".format(prod_id)
-    price = self.db.ReturnRecords(instruction)
-
-    ## Add this data to an instruction template
-    instruction = """
-    INSERT INTO transactions (
-      id,
-      product_id,
-      product_quantity,
-      transaction_datetime
-    )
-    VALUES ({}, {}, {}, datetime('now', 'localtime'))
-    """.format(rowid, prod_id, quantity, price, quantity*price)
-    print(instruction)
-
-    ## Submit instruction to database
-    self.db.TableTransaction(instruction)
-
-  ## Get all items
-  def GetLedger(self):
-    return self.db.ReturnRecords("SELECT * FROM transactions")
-
-  ## Find an item by product id
-  def SortByProductID(self, product_id: int) -> list:
-    instruction = """
-    SELECT * FROM transactions
-    WHERE product_id={}
-    """.format(product_id)
-    return self.db.ReturnRecords(instruction)
-  
-  ## Sort either by date range or a single date
-  def SortByDate(self, furthestdate: str, closestdate=None) -> list:
-    if furthestdate and closestdate:
-      instruction = """
-      SELECT * FROM transactions
-      WHERE transaction_date BETWEEN {} AND {}
-      ORDER BY transaction_date;
-      """.format(furthestdate, closestdate)
-    else:
-      instruction = """
-      SELECT * FROM transactions 
-      WHERE transaction_date={}
-      ORDER BY transaction_date;
-      """.format(furthestdate)
-    return self.db.ReturnRecords(instruction)
-
-  def SortByValue(self):
-    instruction = """
-    SELECT * FROM transactions
-    ORDER BY transaction_value;
-    """
diff --git a/quickpos/product.py b/quickpos/product.py
index 1b662bf..6783c14 100644
--- a/quickpos/product.py
+++ b/quickpos/product.py
@@ -21,6 +21,21 @@ class Product:
     """.format(lastrowid, productname, productprice)
     self.db.TableTransaction(instruction)
 
+  def UpdateProduct(self, record: list):
+    instruction = """
+    UPDATE products
+    SET product_name = '{}', product_price = {}
+    WHERE id = {};
+    """.format(record[1].replace("'", ""), record[2], record[0])
+    self.db.TableTransaction(instruction)
+
+  def DeleteProduct(self, product_id: int):
+    instruction = """
+    DELETE FROM products
+    WHERE id={}
+    """.format(product_id)
+    self.db.TableTransaction(instruction)
+    
   ## Remove the duplicates in the database
   def RemoveDuplicates(self) -> None:
     ## Get all items from a given table
diff --git a/quickpos/server.py b/quickpos/server.py
index 5d07fc7..fe17e82 100644
--- a/quickpos/server.py
+++ b/quickpos/server.py
@@ -1,36 +1,67 @@
-from flask import Flask, render_template, request
+from flask import Flask, render_template, request, redirect
 from quickpos.product import Product
+from quickpos.transaction import Transaction
 app = Flask(__name__)
 
-prod = Product()
-
+## Main page
 @app.route("/")
 def Main():
   return render_template("index.html")
 
-@app.route("/ProductChoiceMenu")
+## Edit and create products section 
+@app.route("/Product")
 def ProductChoiceMenu():
-  return render_template("productchoice.html", productinterface=prod)
+  return render_template("productchoice.html", productinterface=Product)
+
+@app.route("/Product/Edit/<int:product_id>")
+def ProductPage(product_id):
+  prod = Product()
+  prod.RemoveDuplicates()
+  return render_template("product.html", productinterface=Product, product_id=product_id)
 
-@app.route("/Product/<int:product_id>")
-def Product(product_id):
-  return render_template("product.html", productinterface=prod, product_id=product_id)
+@app.route("/Product/Edit/Delete/<int:product_id>")
+def DeleteProduct(product_id):
+  prod = Product()
+  prod.DeleteProduct(product_id)
+  return redirect("/Product")
 
-@app.route("/EditProduct/<int:product_id>", methods=['GET', 'POST'])
+@app.route("/Product/Edit/Send/<int:product_id>", methods=['GET', 'POST'])
 def EditProduct(product_id):
   editedfields = []
-  record = prod.SearchForProduct(product_id)
+  record = list(prod.SearchForProduct(product_id))
   for field in ['prod_name', 'prod_price']:
-    data = request.form[field]
-    if data:
+    if data := request.form[field]:
       editedfields.append(data)
     else:
       editedfields.append('')
   editedfields.insert(0, product_id)
   for i, field in enumerate(record):
     if editedfields[i]:
-      record[i] = editedfield[i]
-  print(record)
+      record[i] = editedfields[i]
+  prod = Product()
+  prod.UpdateProduct(record) 
+  return redirect('/Product')
+
+@app.route("/Product/Create")
+def CreateProduct():
+  return render_template("create.html", productinterface=Product)
+
+@app.route("/Product/Create/Send", methods=['GET', 'POST'])
+def SendNewProduct():
+  record = []
+  for field in ['prod_name', 'prod_price']:
+    if data := request.form[field]:
+      record.append(data)
+    else:
+      return render_template("create.html", productinterface=Product)
+  prod = Product()
+  prod.CreateProduct(record[0], record[1])
+  return redirect('/Product')
+
+## The POS section
+@app.route("/POS")
+def PointOfSale():
+  return render_template("pos.html", productinterface=Product)
 
 if __name__ == "__main__":
   app.run(debug=True)
diff --git a/quickpos/templates/index.html b/quickpos/templates/index.html
index 1386936..0feea98 100644
--- a/quickpos/templates/index.html
+++ b/quickpos/templates/index.html
@@ -11,8 +11,8 @@
 				<h1 class="display-4">QuickPOS</h1>
 			</div>
 		</div>
-		<a href="{{url_for('ProductChoiceMenu')}}" class="btn btn-primary btn-lg">Edit Products</button>
-		<!-- <a href="url_for('pos')" class="btn btn-primary btn-lg">Point of Sale</button>
-		<a href="url_for('insights'" class="btn btn-primary btn-lg">Inventory</button> -->
+		<a href="{{url_for('ProductChoiceMenu')}}" class="btn btn-primary">Edit Products</button>
+		<a href="url_for('PointOfSale')" class="btn btn-primary">Point of Sale</button>
+		<!-- <a href="url_for('insights'" class="btn btn-primary btn-lg">Inventory</button> -->
 	</body>
 </html>
diff --git a/quickpos/templates/pos.html b/quickpos/templates/pos.html
index e69de29..d9cd4f4 100644
--- a/quickpos/templates/pos.html
+++ b/quickpos/templates/pos.html
@@ -0,0 +1,22 @@
+{% set productinterface = productinterface() %}
+{% set product = productinterface.SearchForProduct(product_id) %}
+{% set transaction = transactioninterface() %}
+<!DOCTYPE html>
+<html>
+	<head>
+		<title>
+			Point Of Sale
+		</title>
+	</head>
+	<body>
+		<h1>Point Of Sale</h1>
+		<h3>Items in basket</h3>
+		<ol>
+		{% for item in basket %}
+			<li>item[1]</li>	
+		{% else %}
+			<li>No items in basket</li>
+		{% endfor %)
+		</ol>
+	</body>
+</html>
diff --git a/quickpos/templates/product.html b/quickpos/templates/product.html
index 165f4c1..93c757d 100644
--- a/quickpos/templates/product.html
+++ b/quickpos/templates/product.html
@@ -1,3 +1,4 @@
+{% set productinterface = productinterface() %}
 {% set product = productinterface.SearchForProduct(product_id) %}
 <!DOCTYPE html>
 <html>
@@ -6,11 +7,14 @@
 	</head>
 	<body>
 		<h1>Edit {{ product[1] }}</h1>
-		<form action="{{ url_for('EditProduct', product_id=product[0]) }}" method="post">
-			<p>Product Name</p>
+		<a href="{{ url_for('DeleteProduct', product_id=product[0]) }}">Delete Product</a>
+		<form action="{{ url_for('EditProduct', product_id=product[0]) }}" method="POST">
+			<h4>Product Name</h4>
 			<input type="text" name="prod_name" />
-			<p>Product Price</p>
+			<h4>Product Price</h4>
 			<input type="text" name="prod_price" />
+			<input type="submit" value="Submit">
 		</form>
+			<a href="{{ url_for('Main') }}">Home</a>
 	</body>
 </html>
diff --git a/quickpos/templates/productchoice.html b/quickpos/templates/productchoice.html
index 5582103..055d2e4 100644
--- a/quickpos/templates/productchoice.html
+++ b/quickpos/templates/productchoice.html
@@ -1,16 +1,20 @@
-{% set products = productinterface.GetAllProducts() %}
+{% set prod = productinterface() %}
+{% set products = prod.GetAllProducts() %}
 <!DOCTYPE html>
 <html>
 	<head>
 		<title>Choose Product</title>
+		<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
 	</head>
 	<body>
-		<h1>Choose Product</h1>
-		<h3>Below is a list of editable Products</h3>
+		<h1>Products</h1>
+		<a href="{{ url_for('Main') }}" class="btn btn-primary">Home</a>
+		<a href="{{ url_for('CreateProduct') }}" class="btn btn-primary">Create Product</a>
+		<h3>Edit Products</h3>
 		<ul>
 			{% for product in products %}
 				<li>
-					<a href="{{ url_for('Product', product_id=product[0]) }}">
+					<a href="{{ url_for('ProductPage', product_id=product[0]) }}">
 						{{ product[1] }}
 					</a>
 				</li>
diff --git a/tests/db.py b/tests/db.py
index 4cbd0a2..59e9f82 100644
--- a/tests/db.py
+++ b/tests/db.py
@@ -67,4 +67,4 @@ class Test:
 if __name__ == "__main__":
   t = Test()
   t.Product()
-  t.Transaction()
+  #t.Transaction()
