from database.db_manager import DBManager
from agents.ollama_client import summarize_text

class StoreAgent:
    def __init__(self, store_id: str, db: DBManager):
        self.store_id = store_id
        self.db = db

    def aggregate_store_data(self):
        sql = "SELECT SUM(quantity) FROM sales WHERE product LIKE ?"
        rows = self.db.query(sql, (f"{self.store_id}_%",))
        sales_total = rows[0][0] if rows and rows[0][0] is not None else 0

        sql_inv = "SELECT product, quantity FROM inventory WHERE product LIKE ?"
        inventory = self.db.query(sql_inv, (f"{self.store_id}_%",))
        inv_dict = {row[0]: row[1] for row in inventory}
        return {"sales": sales_total, "inventory": inv_dict}

    def generate_store_report(self):
        data = self.aggregate_store_data()
        report_text = f"Store {self.store_id} report: Sales total is {data['sales']} units, Inventory: {data['inventory']}."
        summary = summarize_text(report_text, model="distilbert")
        return {"store_data": data, "report": summary}

if __name__ == "__main__":
    from database.db_manager import DBManager
    db = DBManager()
    store = StoreAgent("Store_1", db)
    print(store.generate_store_report())
