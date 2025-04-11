from database.db_manager import DBManager
from agents.ollama_client import summarize_text

class InventoryMonitor:
    def __init__(self, db: DBManager):
        self.db = db

    def get_current_inventory(self, product: str):
        sql = "SELECT quantity FROM inventory WHERE product = ?"
        rows = self.db.query(sql, (product,))
        return rows[0][0] if rows else 0

    def check_inventory(self, product: str, threshold: int = 30):
        qty = self.get_current_inventory(product)
        alerts = {}
        if qty < threshold:
            alerts[product] = "Low inventory alert!"
        return qty, alerts

    def generate_alert_report(self, product: str):
        qty, alerts = self.check_inventory(product)
        report_text = f"Current inventory for '{product}' is {qty} units. Alerts: {alerts if alerts else 'None'}."
        # Use DistilBERT for lightweight NLP summarization on this report
        summary = summarize_text(report_text, model="distilbert")
        return {"quantity": qty, "report": summary}

if __name__ == "__main__":
    from database.db_manager import DBManager
    db = DBManager()
    im = InventoryMonitor(db)
    print(im.generate_alert_report("product_A"))
