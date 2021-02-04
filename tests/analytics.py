from quickpos.transaction import Transaction
from quickpos.product import Product

class Test:
  def __init__(self):
    self.tran = Transaction()
    self.prod = Product()

  def CalculateTransactionValues(self):
    totalvalue = 0
    for item in self.tran.GetLedger():
      totalvalue += self.tran.GetTransactionValue(item[0])
    print("Total Earnings:", totalvalue)
    print(self.tran.GetTransaction(1), self.tran.GetTransactionValue(1))

if __name__ == "__main__":
  t = Test()
  t.CalculateTransactionValues()
