import datetime
from database.db_manager import DBManager
from agents.ollama_client import summarize_text

class DemandPredictor:
    def __init__(self, db: DBManager):
        self.db = db

    def load_historical_data(self, product: str):
        sql = "SELECT quantity FROM sales WHERE product = ? ORDER BY sale_date DESC LIMIT 12"
        rows = self.db.query(sql, (product,))
        return [row[0] for row in rows] if rows else []

    def forecast_demand(self, product: str):
        data = self.load_historical_data(product)
        if not data:
            forecast = 0
            confidence = 0.0
        else:
            forecast = sum(data) // len(data)
            confidence = 0.90
        return {"product": product, "forecast": forecast, "confidence": confidence, "timestamp": datetime.datetime.now().isoformat()}

    def generate_report(self, product: str):
        forecast_data = self.forecast_demand(product)
        report_text = (
            f"For product '{product}', the forecasted demand is {forecast_data['forecast']} units "
            f"with {forecast_data['confidence']*100:.1f}% confidence."
        )
        # Use TinyLlama 1.1b for demand forecasting summaries
        summary = summarize_text(report_text, model="tinyllama-1.1b")
        return {"forecast": forecast_data["forecast"], "report": summary}

if __name__ == "__main__":
    db = DBManager()
    dp = DemandPredictor(db)
    print(dp.generate_report("product_A"))
