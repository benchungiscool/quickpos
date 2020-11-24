from database import Database

# Test
dbName = "items"
tableName = "products"
start = """
CREATE TABLE IF NOT EXISTS {} (
    [prid] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [name] TEXT NOT NULL,
    [price] INTEGER NOT NULL,
);
""".format("products")

returnall = """
SELECT * 
FROM {}
""".format(tableName)

products = [
    ("Sausages", 1.50, "Saus1"),
    ("Wotsits", 0.5, "Wots1"),
    ("Bananas", 0.25, "Bana1"),
    ("Playboy Magazine", 5, "Maga1")
]

if __name__ == "__main__":  
    db = Database(dbName, tableName, start)

    for product in products:

        insertion = """
        INSERT INTO {}
        VALUES {}
        """.format(tableName, product)

        for record in range(20):
            db.TableTransaction(insertion)

    for record in db.ReturnRecords(returnall):
        print(record)
    
    print("\n")
    db.Clear()

    for record in db.ReturnRecords(returnall):
        print(record)