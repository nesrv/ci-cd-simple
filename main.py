import os
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "user": os.getenv("DB_USER", "app"),
    "password": os.getenv("DB_PASSWORD", "app"),
    "dbname": os.getenv("DB_NAME", "eshop"),
}


def get_db_connection():
    """Подключение к PostgreSQL (psycopg v3)."""
    return psycopg.connect(**DB_CONFIG, row_factory=dict_row)


def run_query(query: str, params=None, one=False):
    """Выполнить запрос и вернуть результат. one=True — одна строка или None."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if one:
                return cur.fetchone()
            return cur.fetchall()
    finally:
        conn.close()


def run_command(query: str, params=None):
    """Выполнить команду без возврата результата."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
        conn.commit()
    finally:
        conn.close()


class Product(BaseModel):
    name: str
    price: float
    description: str
    created_at: str


class CartItem(BaseModel):
    product_name: str
    quantity: int
    price: float


app = FastAPI(title="E-Shop-СI-CD-part-2.0.2")


def _row_to_product(r):
    if not r:
        return None
    return {
        "id": r["id"],
        "name": r["name"],
        "price": float(r["price"]),
        "description": r["description"] or "",
        "created_at": r["created_at"].isoformat() if r["created_at"] else "",
    }


@app.get("/products")
async def get_products():
    """Список видеокарт из БД (функция get_products())."""
    rows = run_query("SELECT * FROM get_products()")
    return [_row_to_product(r) for r in rows]


@app.get("/product/{pid}")
async def get_product(pid: int):
    """Один товар по индексу 0-based (функция get_product_by_index)."""
    row = run_query("SELECT * FROM get_product_by_index(%s)", (pid,), one=True)
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    return _row_to_product(row)


@app.get("/search")
async def search(q: str = Query(..., min_length=1)):
    """Поиск по названию (функция search_products)."""
    rows = run_query("SELECT * FROM search_products(%s)", (q,))
    return [_row_to_product(r) for r in rows]


@app.get("/cart")
async def get_cart():
    """Корзина из БД (функция get_cart_items)."""
    rows = run_query("SELECT * FROM get_cart_items()")
    items = [{"name": r["product_name"], "qty": r["qty"], "price": float(r["price"])} for r in rows]
    total = sum(i["price"] for i in items)
    return {"items": items, "total": total}


@app.post("/cart/add")
async def add_cart(pid: int, qty: int = 1):
    """Добавить в корзину по индексу товара 0-based (add_to_cart)."""
    product_id = run_query("SELECT get_product_id_by_index(%s)", (pid,), one=True)
    if not product_id or product_id["get_product_id_by_index"] is None:
        raise HTTPException(status_code=404, detail="Not found")
    run_command("SELECT add_to_cart(%s, %s)", (product_id["get_product_id_by_index"], qty))
    return {"ok": True}


@app.delete("/cart")
async def clear_cart():
    """Очистить корзину (функция clear_cart)."""
    run_command("SELECT clear_cart()")
    return {"ok": True}


@app.post("/checkout")
async def checkout():
    """Оформить заказ (функция checkout)."""
    row = run_query("SELECT checkout() AS result", one=True)
    if not row or row["result"] is None:
        raise HTTPException(status_code=400, detail="Cart is empty")
    o = row["result"]
    if hasattr(o, "items"):
        return dict(o)
    return o


@app.get("/orders")
async def get_orders():
    """Список заказов из БД (функция get_orders)."""
    rows = run_query("SELECT * FROM get_orders()")
    result = []
    for r in rows:
        val = r["get_orders"] if "get_orders" in r else r
        if hasattr(val, "items"):
            result.append(dict(val))
        else:
            result.append(val)
    return result


@app.get("/health")
async def health():
    """Проверка приложения и БД (db_ping, количество товаров)."""
    db_ok = False
    products_count = 0
    try:
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT db_ping()")
            cur.fetchone()
            cur.execute("SELECT COUNT(*) AS cnt FROM get_products()")
            products_count = cur.fetchone()["cnt"] or 0
            db_ok = True
        finally:
            conn.close()
    except Exception:
        pass
    return {
        "status": "ok",
        "products": products_count,
        "database": "ok" if db_ok else "error",
    }
