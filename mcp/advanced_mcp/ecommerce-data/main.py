from fastapi import FastAPI, HTTPException
from datetime import date, timedelta

app = FastAPI()


# =====================================================
# FAKE ORDER DATABASE
# =====================================================

fake_orders = {
    1: {
        "customer_id": 1,
        "item_name": "Laptop",
        "expected_delivery_date": date.today() - timedelta(days=10),
        "delivery_status": "Lost in transit",
        "delayed_days": 10
    },

    2: {
        "customer_id": 2,
        "item_name": "Headphones",
        "expected_delivery_date": date.today() + timedelta(days=5),
        "delivery_status": "Shipped",
        "delayed_days": 0
    },

    3: {
        "customer_id": 3,
        "item_name": "Book",
        "expected_delivery_date": date.today() + timedelta(days=1),
        "delivery_status": "Arriving tomorrow",
        "delayed_days": 0
    },

    4: {
        "customer_id": 4,
        "item_name": "Smartphone",
        "expected_delivery_date": date.today() - timedelta(days=2),
        "delivery_status": "Delivered",
        "delayed_days": 0,
        "delivered_date": date.today() - timedelta(days=2),
        "item_condition": "Damaged"
    },

    5: {
        "customer_id": 5,
        "item_name": "Keyboard",
        "expected_delivery_date": date.today() - timedelta(days=4),
        "delivery_status": "Delayed",
        "delayed_days": 4
    },

    6: {
        "customer_id": 6,
        "item_name": "Monitor",
        "expected_delivery_date": date.today() - timedelta(days=9),
        "delivery_status": "Delayed",
        "delayed_days": 9
    }
}


# =====================================================
# DELIVERY ENDPOINT
# =====================================================

@app.get("/delivery/{customer_id}")
def get_delivery(customer_id: int):
    """
    Return order information for a customer.

    This endpoint is used by the MCP get_order_data tool.
    """

    if customer_id not in fake_orders:
        raise HTTPException(
            status_code=404,
            detail="Order data not found"
        )

    return fake_orders[customer_id]