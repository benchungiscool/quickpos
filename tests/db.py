
import backend.database


# Test
class DBTest:

    ## Define some key commands
    

    self.returnall = """
    SELECT * 
    FROM {}
    """.format(tableName)

def __init__(self):
    dbName = "items"
    tableName = "products"
    products = [
        ("Sausages", 0.50),
        ("Wotsits", -1.5),
        ("Bananas", -1.25),
        ("Playboy Magazine", 4)
    ]

    if __name__ == "__main__":  
        db = Database(dbName, tableName, start)

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
