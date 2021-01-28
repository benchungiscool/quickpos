from quickpos.transaction import Transaction
from quickpos.product import Product

class Test:
  def __init__(self):
    self.tran = Transaction()
    self.prod = Product()

  def CalculateTransactionValues(self):
    for i in self.tran.GetLedger():
      print(i, self.tran.GetTransactionValue(i[0]))

if __name__ == "__main__":
  t = Test()
  t.CalculateTransactionValues()
