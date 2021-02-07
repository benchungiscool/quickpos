from flask import Flask, render_template, request, redirect
from quickpos.product import Product
from quickpos.transaction import Transaction
app = Flask(__name__)

basket = []

## Main page
@app.route("/")
def Main():
  return render_template("index.html")

## Edit and create products section 
@app.route("/Product")
def ProductChoiceMenu():
  return render_template("productchoice.html", productinterface=Product)

@app.route("/Product/Edit/<int:product_id>")
def ProductPage(product_id):
  prod = Product()
  prod.RemoveDuplicates()
  return render_template("product.html", productinterface=Product, product_id=product_id)

@app.route("/Product/Edit/Delete/<int:product_id>")
def DeleteProduct(product_id):
  prod = Product()
  prod.DeleteProduct(product_id)
  return redirect("/Product")

@app.route("/Product/Edit/Send/<int:product_id>", methods=['GET', 'POST'])
def EditProduct(product_id):
  editedfields = []
  prod = Product()
  record = list(prod.SearchForProduct(product_id))
  for field in ['prod_name', 'prod_price']:
    if data := request.form[field]:
      editedfields.append(data)
    else:
      editedfields.append('')
  editedfields.insert(0, product_id)
  for i, field in enumerate(record):
    if editedfields[i]:
      record[i] = editedfields[i]
  prod.UpdateProduct(record) 
  return redirect('/Product')

@app.route("/Product/Create")
def CreateProduct():
  return render_template("create.html", productinterface=Product)

@app.route("/Product/Create/Send", methods=['GET', 'POST'])
def SendNewProduct():
  record = []
  for field in ['prod_name', 'prod_price']:
    if data := request.form[field]:
      record.append(data)
    else:
      return render_template("create.html", productinterface=Product)
  prod = Product()
  prod.CreateProduct(record[0], record[1])
  return redirect('/Product')

## The POS section
@app.route("/POS")
def PointOfSale():
  prod = Product()
  products = prod.GetAllProducts()
  if not basket:
    return render_template("pos.html", products=products, t=Transaction)
  else:
    return render_template("pos.html", products=products, basket=basket, t=Transaction)

@app.route("/POS/<int:prid>")
def AddToBasket(prid):
  basket.append(Product().SearchForProduct(prid))
  return redirect("/POS")

@app.route("/POS/Clear")
def ClearBasket():
  basket = []
  return redirect("/POS")

if __name__ == "__main__":
  app.run(debug=True)

