from flask import Flask, render_template
from quickpos.product import Product
app = Flask(__name__)

prod = Product()
prodtablecontents = prod.GetAllProducts()
for i in prodtablecontents:
  print(i)

@app.route("/")
def Main():
  return render_template("index.html")

@app.route("/ProductChoiceMenu")
def ProductChoiceMenu():
  return render_template("productchoice.html", products=prodtablecontents)

@app.route("/Product/<int:product_id>")
def Product(product_id):
  record = prod.SearchForProduct(product_id)
  return render_template("product.html", product=record)

@app.route("/EditProduct", methods=['GET', 'POST'])
def EditProduct():
  data = request.form.get()
  print(data)

if __name__ == "__main__":
  app.run(debug=True)

