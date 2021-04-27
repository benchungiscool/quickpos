from quickpos.transaction import Transaction
from quickpos.product import Product

class Test:
  def __init__(self):
    self.tr = Transaction()
    self.prod = Product()

  def CalculateTransactionValues(self):
    totalvalue = 0
    for item in self.tr.GetLedger():
      totalvalue += self.tr.GetTransactionValue(item[0])
    print("Total Earnings:", totalvalue)
    print(self.tr.GetTransaction(1), self.tr.GetTransactionValue(1))

  def CalculateTimeLeft(self):
    for item in products := self.pr

if __name__ == "__main__":
  t = Test()
  t.CalculateTransactionValues()
