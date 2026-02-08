from __future__ import annotations

import json
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from pathlib import Path

class Product(BaseModel):
    name: str
    price: float
    description: str
    created_at: str

class CartItem(BaseModel):
    product_name: str
    quantity: int
    price: float

app = FastAPI(title="E-Shop")
with open(Path(__file__).parent / "shop.json", "r", encoding="utf-8") as f:
    PRODUCTS: list[dict] = json.load(f)

CART: list[dict] = []
ORDERS: list[dict] = []

@app.get("/products")
async def get_products() -> list[dict]:
    return PRODUCTS

@app.get("/product/{pid}")
async def get_product(pid: int) -> dict:
    if 0 <= pid < len(PRODUCTS):
        return PRODUCTS[pid]
    raise HTTPException(status_code=404, detail="Not found")

@app.get("/search")
async def search(q: str = Query(..., min_length=1)) -> list[dict]:
    return [p for p in PRODUCTS if q.lower() in p["name"].lower()]

@app.get("/cart")
async def get_cart() -> dict:
    return {"items": CART, "total": sum(i["price"] for i in CART)}

@app.post("/cart/add")
async def add_cart(pid: int, qty: int = 1) -> dict:
    if not (0 <= pid < len(PRODUCTS)):
        raise HTTPException(status_code=404)
    p = PRODUCTS[pid]
    CART.append({"name": p["name"], "qty": qty, "price": p["price"] * qty})
    return {"ok": True}

@app.delete("/cart")
async def clear_cart() -> dict:
    CART.clear()
    return {"ok": True}

@app.post("/checkout")
async def checkout() -> dict:
    if not CART:
        raise HTTPException(status_code=400)
    total = sum(i["price"] for i in CART)
    order = {"items": CART.copy(), "total": total, "date": datetime.now().isoformat()}
    ORDERS.append(order)
    CART.clear()
    return order

@app.get("/orders")
async def get_orders() -> list[dict]:
    return ORDERS

@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "products": len(PRODUCTS)}

