import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    """Проверка endpoint /health"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_products():
    """Проверка endpoint /products"""
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_product_by_id():
    """Проверка получения товара по ID"""
    response = client.get("/product/0")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "price" in data


def test_product_not_found():
    """Проверка ошибки при неправильном ID"""
    response = client.get("/product/9999")
    assert response.status_code == 404


def test_search():
    """Проверка поиска по названию"""
    response = client.get("/search?q=RTX")
    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)


def test_cart_empty():
    """Проверка пустой корзины"""
    # Сначала очищаем корзину
    client.delete("/cart")
    response = client.get("/cart")
    assert response.status_code == 200
    assert response.json()["items"] == []
    assert response.json()["total"] == 0


def test_add_to_cart():
    """Проверка добавления в корзину"""
    client.delete("/cart")  # Очищаем
    response = client.post("/cart/add?pid=0&qty=1")
    assert response.status_code == 200

    # Проверяем что товар в корзине
    cart = client.get("/cart").json()
    assert len(cart["items"]) == 1


def test_checkout():
    """Проверка оформления заказа"""
    client.delete("/cart")  # Очищаем

    # Добавляем товар
    client.post("/cart/add?pid=0&qty=2")

    # Оформляем заказ
    response = client.post("/checkout")
    assert response.status_code == 200
    order = response.json()
    assert "items" in order
    assert "total" in order
    assert len(order["items"]) > 0

    # Проверяем что корзина очищена
    cart = client.get("/cart").json()
    assert len(cart["items"]) == 0


def test_orders():
    """Проверка получения списка заказов"""
    response = client.get("/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
