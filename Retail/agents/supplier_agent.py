from database.db_manager import DBManager
from agents.ollama_client import summarize_text

class SupplierAgent:
    def __init__(self, db: DBManager):
        self.db = db

    def process_supplier_order(self, order_details: dict):
        return f"Order for {order_details} confirmed."

    def generate_supplier_report(self, order_details: dict):
        confirmation = self.process_supplier_order(order_details)
        report_text = f"Supplier Order Report: {confirmation}"
        summary = summarize_text(report_text, model="distilbert")
        return {"order_details": order_details, "confirmation": confirmation, "report": summary}

if __name__ == "__main__":
    from database.db_manager import DBManager
    db = DBManager()
    sa = SupplierAgent(db)
    order_details = {"product_A": 50, "product_B": 30}
    print(sa.generate_supplier_report(order_details))
