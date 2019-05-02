import sys
sys.path.append("d:/bismuth_foundation")
import essentials
import sqlite3
from hashlib import blake2b

coordinator = "fefb575972cd8fdb086e2300b51f727bb0cbfc33282f1542e19a8f1d"
operation_init = "prediction:open"
operation_pred = "prediction:make"

class DbHandler():
    def __init__(self):
        self.database = sqlite3.connect("D:/bismuth_foundation/static/ledger.db")
        self.database.text_factory = str
        self.cursor = self.database.cursor()

    def events_db_init(self):
        self.prediction_database = sqlite3.connect("prediction.db")
        self.prediction_cursor = self.prediction_database.cursor()

class Events():
    def assign_init(self,data):
        formatted = essentials.format_raw_tx(data)
        openfield = formatted["openfield"].split(";")

        assigned = {} #prevent misformatting
        try:
            for part in openfield:
                x = (part.split(":"))
                assigned[x[0]] = x[1]

            self.event = assigned["event"]
            self.until = assigned["until"]
            self.oracle = assigned["oracle"]
            self.results = assigned["results"].split(",")

            print(self.event,self.until,self.oracle,self.results)
        except:

            print (f"Problem assigning values for {openfield}")


    def seek_init(self):
        db_handler.cursor.execute("SELECT * FROM transactions WHERE recipient = ? AND operation = ?",(coordinator, operation_init,))
        transactions = db_handler.cursor.fetchall()
        for tx in transactions:
            blake2bhash = blake2b(str(tx).encode(), digest_size=20).hexdigest()
            print("tx",tx)
            self.assign_init(tx)

class Predictions():
    def assign_preds(self,data):
        formatted = essentials.format_raw_tx(data)
        openfield = formatted["openfield"].split(";")
        assigned = {}
        try:
            for part in openfield:
                x = (part.split(":"))
                assigned[x[0]] = x[1]

            self.event = assigned["event"]
            self.result = assigned["result"]

            print (self.event,self.result)

        except:
            print (f"Problem assigning values for {openfield}")

    def seek_preds(self):
        db_handler.cursor.execute("SELECT * FROM transactions WHERE recipient = ? AND operation = ?",(coordinator, operation_pred,))
        transactions = db_handler.cursor.fetchall()

        for tx in transactions:
            blake2bhash = blake2b(str(tx).encode(), digest_size=20).hexdigest()
            print("tx",tx)
            self.assign_preds(tx)

if __name__ == "__main__":
    db_handler = DbHandler()
    db_handler.events_db_init()

    events = Events()
    preds = Predictions()

    events.seek_init()
    preds.seek_preds()
