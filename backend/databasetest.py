from backend.database import Database
from backend.product import Product

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

  prod.RemoveDuplicates("products")

