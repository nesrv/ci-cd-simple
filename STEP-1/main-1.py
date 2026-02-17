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

app = FastAPI(title="E-Shop-СI-CD")
with open(Path(__file__).parent / "shop.json", "r", encoding="utf-8") as f:
    PRODUCTS = json.load(f)

CART = []
ORDERS = []

# --- Эндпоинты каталога ---

@app.get("/products")
async def get_products():
    """Возвращает список всех товаров из каталога (shop.json)."""
    return PRODUCTS

@app.get("/product/{pid}")
async def get_product(pid: int):
    """Возвращает один товар по числовому id (индексу). 404, если id вне диапазона."""
    if 0 <= pid < len(PRODUCTS):
        return PRODUCTS[pid]
    raise HTTPException(status_code=404, detail="Not found")

@app.get("/search")
async def search(q: str = Query(..., min_length=1)):
    """Поиск товаров по подстроке в названии (q). Регистр не учитывается."""
    return [p for p in PRODUCTS if q.lower() in p["name"].lower()]

# --- Эндпоинты корзины ---

@app.get("/cart")
async def get_cart():
    """Возвращает содержимое корзины и общую сумму."""
    return {"items": CART, "total": sum(i["price"] for i in CART)}

@app.post("/cart/add")
async def add_cart(pid: int, qty: int = 1):
    """Добавляет товар в корзину по id (pid) и количеству (qty). 404 при неверном pid."""
    if not (0 <= pid < len(PRODUCTS)):
        raise HTTPException(status_code=404)
    p = PRODUCTS[pid]
    CART.append({"name": p["name"], "qty": qty, "price": p["price"] * qty})
    return {"ok": True}

@app.delete("/cart")
async def clear_cart():
    """Очищает корзину полностью."""
    CART.clear()
    return {"ok": True}

# --- Эндпоинты заказов ---

@app.post("/checkout")
async def checkout():
    """Оформляет заказ: сохраняет текущую корзину в заказы, очищает корзину. 400 если корзина пуста."""
    if not CART:
        raise HTTPException(status_code=400)
    total = sum(i["price"] for i in CART)
    order = {"items": CART.copy(), "total": total, "date": datetime.now().isoformat()}
    ORDERS.append(order)
    CART.clear()
    return order

@app.get("/orders")
async def get_orders():
    """Возвращает список всех оформленных заказов."""
    return ORDERS

# --- Служебный эндпоинт ---

@app.get("/health")
async def health():
    """Проверка живости сервиса: статус и количество товаров в каталоге (для CI/CD/мониторинга)."""
    return {"status": "ok", "products": len(PRODUCTS)}

