from django.shortcuts import render
from database.db_manager import DBManager
from agents.demand_predictor import DemandPredictor
from agents.inventory_monitor import InventoryMonitor
from agents.pricing_optimizer import PricingOptimizer
from agents.store_agent import StoreAgent
from agents.warehouse_agent import WarehouseAgent
from agents.supplier_agent import SupplierAgent
from agents.customer_agent import CustomerAgent

def dashboard_home(request):
    db = DBManager()
    # Initialize agents
    dp = DemandPredictor(db)
    im = InventoryMonitor(db)
    po = PricingOptimizer(db)
    store = StoreAgent("Store_1", db)
    wa = WarehouseAgent(db)
    sa = SupplierAgent(db)
    ca = CustomerAgent(db)

    product = "product_A"
    demand_report = dp.generate_report(product)
    inventory_report = im.generate_alert_report(product)
    pricing_report = po.generate_pricing_report(product, demand_report, inventory_report["quantity"])
    store_report = store.generate_store_report()
    warehouse_report = wa.generate_warehouse_report()
    supplier_report = sa.generate_supplier_report({"product_A": 50, "product_B": 30})
    customer_report = ca.generate_customer_report(product)

    context = {
        "demand_report": demand_report,
        "inventory_report": inventory_report,
        "pricing_report": pricing_report,
        "store_report": store_report,
        "warehouse_report": warehouse_report,
        "supplier_report": supplier_report,
        "customer_report": customer_report,
    }
    return render(request, "dashboard/dashboard_home.html", context)
