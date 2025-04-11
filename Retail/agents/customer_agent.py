from database.db_manager import DBManager
from agents.ollama_client import summarize_text

class CustomerAgent:
    def __init__(self, db: DBManager):
        self.db = db

    def gather_customer_feedback(self, product: str):
        sql = "SELECT feedback FROM customer_feedback WHERE product = ? ORDER BY created_at DESC LIMIT 1"
        rows = self.db.query(sql, (product,))
        return rows[0][0] if rows else "No feedback available."

    def analyze_sentiment(self, feedback: str):
        return "negative" if "bad" in feedback.lower() else "positive"

    def generate_customer_report(self, product: str):
        feedback = self.gather_customer_feedback(product)
        sentiment = self.analyze_sentiment(feedback)
        report_text = f"Feedback for '{product}': '{feedback}' indicates a {sentiment} sentiment."
        summary = summarize_text(report_text, model="distilbert")
        return {"feedback": feedback, "sentiment": sentiment, "report": summary}

if __name__ == "__main__":
    from database.db_manager import DBManager
    db = DBManager()
    ca = CustomerAgent(db)
    print(ca.generate_customer_report("product_A"))
