from flask import Flask, render_template, request
from quickpos.product import Product
app = Flask(__name__)

prod = Product()

@app.route("/")
def Main():
  return render_template("index.html")

@app.route("/ProductChoiceMenu")
def ProductChoiceMenu():
  return render_template("productchoice.html", productinterface=prod)

@app.route("/Product/<int:product_id>")
def Product(product_id):
  return render_template("product.html", productinterface=prod, product_id=product_id)

@app.route("/EditProduct/<int:product_id>", methods=['GET', 'POST'])
def EditProduct(product_id):
  editedfields = []
  record = prod.SearchForProduct(product_id)
  for field in ['prod_name', 'prod_price']:
    data = request.form[field]
    if data:
      editedfields.append(data)
    else:
      editedfields.append('')
  editedfields.insert(0, product_id)
  for i, field in enumerate(record):
    if editedfields[i]:
      record[i] = editedfield[i]
  print(record)

if __name__ == "__main__":
  app.run(debug=True)

