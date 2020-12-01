import init
from backend.database import Database
from backend.queries import Queries

# Test
class DBTest:

    def __init__(self):
        dbName = "items"
        tableName = "products"
        products = [
            ("Sausages", 0.50),
            ("Wotsits", 1.5),
            ("Bananas", 1.25),
            ("Playboy Magazine", 4)
        ]

        if __name__ == "__main__":  
            db = Database(db, dbName, tableName, Queries.ProductTable())

            for product in products:

                insertion = """
                INSERT INTO {} {}
                VALUES {}
                """.format(tableName, "(name, price)", product)

                for record in range(19):
                    db.TableTransaction(insertion)

            for record in db.ReturnRecords(returnall):
                print(record)
            
            print("\n")
            db.Clear()

            for record in db.ReturnRecords(returnall):
                print(record)

if __name__ == "__main__":
    tablename = Queries("products")
    db = DBTest()
