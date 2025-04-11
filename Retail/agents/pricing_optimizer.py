from database.db_manager import DBManager
from agents.ollama_client import summarize_text

class PricingOptimizer:
    def __init__(self, db: DBManager):
        self.db = db

    def get_current_price(self, product: str):
        sql = "SELECT price FROM prices WHERE product = ?"
        rows = self.db.query(sql, (product,))
        return rows[0][0] if rows else 0.0

    def optimize_price(self, product: str, demand_forecast: int, current_inventory: int):
        base_price = self.get_current_price(product)
        adjustment = 1.0 if demand_forecast > current_inventory else -1.0
        new_price = max(base_price + adjustment, 0.0)
        return new_price

    def generate_pricing_report(self, product: str, forecast_data: dict, current_inventory: int):
        new_price = self.optimize_price(product, forecast_data["forecast"], current_inventory)
        report_text = f"For '{product}', the recommended new price is ${new_price:.2f}."
        # Use Gemma2b_phi2_flan_t5_small for this pricing summary
        summary = summarize_text(report_text, model="gemma2b_phi2_flan_t5_small")
        return {"new_price": new_price, "report": summary}

if __name__ == "__main__":
    from database.db_manager import DBManager
    db = DBManager()
    po = PricingOptimizer(db)
    forecast_data = {"forecast": 100}
    print(po.generate_pricing_report("product_A", forecast_data, 25))
