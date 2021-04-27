from flask import Flask, render_template, request, redirect
from quickpos.product import Product
from quickpos.transaction import Transaction
app = Flask(__name__)

## Products for a transaction go in here
basket = []

## Homepage
@app.route("/")
def Main():
  ## Return the rendered main page
  return render_template("index.html")

## List of products which leads to create and edit product pages
@app.route("/Product")
def ProductChoiceMenu():
  ## Remove duplicate items
  prod = Product()
  prod.RemoveDuplicates()
  for i in prod.GetAllProducts():
    print(i)
  ## Return rendered product choice page, pass in instance of Product class
  return render_template("productchoice.html", productinterface=Product)

## Returns a page which allows the user to edit and create products
@app.route("/Product/Edit/<int:product_id>")
def ProductPage(product_id):
  prod = Product()
  ## Render template with product interface, the id of the product in question and information
  ## About how long the product will last for
  return render_template("product.html", productinterface=Product, product_id=product_id, 
                         daysleft=Transaction().DaysProductLeft(product_id))

## Remove item from products table
@app.route("/Product/Edit/Delete/<int:product_id>")
def DeleteProduct(product_id):
  ## Remove the given product id from the database table
  prod = Product()
  prod.DeleteProduct(product_id)
  ## Redirect back to the product choice menu
  return redirect("/Product")

## Update an existing record for a product
@app.route("/Product/Edit/Send/<int:product_id>", methods=['POST'])
def EditProduct(product_id):
  editedfields = []
  prod = Product()
  record = list(prod.GetProduct(product_id))
  ## Iterate over values given in name and price
  for field in ['prod_name', 'prod_price']:
    ## If there is a value in field, add to editedfieldsj
    if data := request.form[field]:
      editedfields.append(data)
    else:
      ## Otherwise, leave empty value
      editedfields.append('')
  ## Add empty value to the start of edited field
  editedfields.insert(0, product_id)
  ## Iterate over current record for product
  for i, field in enumerate(record[:-1]):
    ## If this field has changed, put in record
    if editedfields[i]:
      record[i] = editedfields[i]
  ## Update the product
  prod.UpdateProduct(*record[:-1]) 
  ## If stock has changed, send this to database
  if data := request.form['prod_stock']:
    prod.ChangeStockLevel(product_id, int(data))
  ## Redirect to product page
  return redirect('/Product')

## Returns the form to create a product
@app.route("/Product/Create")
def CreateProduct():
  ## Return the form
  return render_template("create.html")

## Send a product created by the create product form to the products table
@app.route("/Product/Create/Send", methods=['POST'])
def SendNewProduct():
  record = []
  ## For each field in the form
  for field in ['prod_name', 'prod_price', 'prod_stock']:
    ## If data is in a request field, append to the record  
    if data := request.form[field]:
      record.append(data)
    ## Otherwise, make them do the form again
    else:
      return redirect("/Product/Create")
  ## Send the new product to the database
  prod = Product()
  prod.CreateProduct(*record)
  ## Redirect to product menu
  return redirect('/Product')

## The POS section
@app.route("/POS")
def PointOfSale():
  ## Remove duplicate records from product table
  prod = Product()
  prod.RemoveDuplicates()
  for i in Transaction().GetAllTransactions():
    print(i)
  ## Get all products from the database
  products = list(filter(lambda x: x[3] > 0, prod.GetAllProducts()))
  if basket:
    ## Generate a price for the items in basket
    price = sum(list(map(lambda x: x[0][2] * x[1], basket)))
    ## Return a page that is formatted with the basket and price
    return render_template("pos.html", products=products, basket=basket, price=price)
  ## If no item in basket, return a page formatted with products for buttons
  return render_template("pos.html", products=products)

## Add a given item to the basket
@app.route("/POS/Add/<int:prid>")
def AddToBasket(prid):
  global basket
  ## Get the record for the product
  product = Product().GetProduct(prid)
  ## If the item isn't in the basket, add with product record and starting quantity of 1
  if product not in map(lambda x: x[0], basket):
    basket.append([product, 1])
  ## Otherwise, just increment the quantity
  else:
    basket[list(map(lambda x: x[0], basket)).index(product)][1] += 1
  ## Redirect back to point of sale terminal
  return redirect("/POS")

## Remove a given item from a transaction
@app.route("/POS/Remove/<int:item>")
def RemoveItem(item: int):
  global basket
  ## Search for record in basket
  location = list(map(lambda x: x[0], basket)).index(Product().GetProduct(item))
  ## If only one item in basket, remove from the basket completely
  if basket[location][1] == 1:
    basket.pop(location)
  ## Otherwise, change the amount of items in basket by -1
  else:
    basket[location][1] -= 1
  ## Redirect to the point of sale terminal
  return redirect("/POS")

## Remove all items from the basket
@app.route("/POS/Clear")
def ClearBasket():
  global basket
  ## Define basket as an empty list
  basket = []
  ## Redirect to point of sale terminal
  return redirect("/POS")

## Send a transaction to the database
@app.route("/POS/Send")
def SendTransaction():
  ## Change data items to lists of product ids and quantites, send to database
  tran = Transaction()  
  tran.RecordTransaction(*list(map(lambda x: [x[0][0], x[1]], basket)))
  ## Clear basket, and redirect to the point of sale terminal
  return redirect("/POS/Clear")

## Main loop
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)

