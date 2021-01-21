from backend.database import Database


class Transaction:
  def __init__(self):
    self.db = Database()
    
  def RecordTransaction(self, productid: int, productquantity: int, productprice: float):
    instruction = """
    INSERT INTO transactions ()
    """
