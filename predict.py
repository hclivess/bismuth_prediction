import sys
sys.path.append("d:/bismuth_foundation")
import essentials
import sqlite3

coordinator = "fefb575972cd8fdb086e2300b51f727bb0cbfc33282f1542e19a8f1d"
operation = "predict:open"

class DbHandler():
    def __init__(self):
        self.database = sqlite3.connect("D:/bismuth_foundation/static/ledger.db")
        self.database.text_factory = str
        self.cursor = self.database.cursor()

class Predictor():

    def assign(self,data):
        for part in data:
            x = (part.split(":"))
            print(x)

    def split(self, data):
        for part in data:
            formatted = essentials.format_raw_tx(part)

            openfield = formatted["openfield"].split(";")
            print(openfield)
            self.assign(openfield)





    def seek(self):
        db_handler.cursor.execute("SELECT * FROM transactions WHERE recipient = ? AND operation = ?",(coordinator, operation,))
        results = db_handler.cursor.fetchall()

        self.split(results)



db_handler = DbHandler()
predictor = Predictor()

predictor.seek()
