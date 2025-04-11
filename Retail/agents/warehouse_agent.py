from database.db_manager import DBManager
from agents.ollama_client import summarize_text

class WarehouseAgent:
    def __init__(self, db: DBManager):
        self.db = db

    def aggregate_warehouse_data(self):
        sql = "SELECT product, quantity FROM inventory"
        rows = self.db.query(sql)
        inventory = {row[0]: row[1] for row in rows}
        return {"total_inventory": inventory}

    def schedule_restock(self, inventory, threshold=250):
        orders = {}
        for product, qty in inventory["total_inventory"].items():
            if qty < threshold:
                orders[product] = 300 - qty
        return orders

    def generate_warehouse_report(self):
        inventory = self.aggregate_warehouse_data()
        orders = self.schedule_restock(inventory)
        report_text = f"Warehouse inventory: {inventory}. Restock orders: {orders if orders else 'None'}."
        summary = summarize_text(report_text, model="distilbert")
        return {"warehouse_inventory": inventory, "restock_orders": orders, "report": summary}

if __name__ == "__main__":
    from database.db_manager import DBManager
    db = DBManager()
    wa = WarehouseAgent(db)
    print(wa.generate_warehouse_report())
