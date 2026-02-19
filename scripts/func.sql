-- Таблицы для корзины и заказов, хранимые функции для эндпоинтов.
-- Выполнять после scripts/init_db.sql (должна существовать таблица video_cards).

CREATE TABLE IF NOT EXISTS cart (
    id          BIGSERIAL PRIMARY KEY,
    product_id  BIGINT NOT NULL REFERENCES video_cards(id),
    qty         INT NOT NULL DEFAULT 1,
    created_at  TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS orders (
    id          BIGSERIAL PRIMARY KEY,
    total       NUMERIC(12,2) NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS order_items (
    order_id    BIGINT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_name TEXT NOT NULL,
    qty         INT NOT NULL,
    price       NUMERIC(12,2) NOT NULL
);

-- Список всех видеокарт
CREATE OR REPLACE FUNCTION get_products()
RETURNS TABLE(id bigint, name text, price numeric, description text, created_at timestamptz)
LANGUAGE sql STABLE AS $$
    SELECT v.id, v.name, v.price, v.description, v.created_at
    FROM video_cards v
    ORDER BY v.id;
$$;

-- Один товар по id
CREATE OR REPLACE FUNCTION get_product(p_id bigint)
RETURNS TABLE(id bigint, name text, price numeric, description text, created_at timestamptz)
LANGUAGE sql STABLE AS $$
    SELECT v.id, v.name, v.price, v.description, v.created_at
    FROM video_cards v
    WHERE v.id = p_id;
$$;

-- Один товар по индексу (0-based), для совместимости с API /product/0
CREATE OR REPLACE FUNCTION get_product_by_index(p_idx int)
RETURNS TABLE(id bigint, name text, price numeric, description text, created_at timestamptz)
LANGUAGE sql STABLE AS $$
    SELECT v.id, v.name, v.price, v.description, v.created_at
    FROM video_cards v
    ORDER BY v.id
    LIMIT 1 OFFSET GREATEST(0, p_idx);
$$;

-- id товара по индексу (0-based), для add_to_cart
CREATE OR REPLACE FUNCTION get_product_id_by_index(p_idx int)
RETURNS bigint
LANGUAGE sql STABLE AS $$
    SELECT v.id FROM video_cards v ORDER BY v.id LIMIT 1 OFFSET GREATEST(0, p_idx);
$$;

-- Поиск по названию
CREATE OR REPLACE FUNCTION search_products(query text)
RETURNS TABLE(id bigint, name text, price numeric, description text, created_at timestamptz)
LANGUAGE sql STABLE AS $$
    SELECT v.id, v.name, v.price, v.description, v.created_at
    FROM video_cards v
    WHERE v.name ILIKE '%' || query || '%'
    ORDER BY v.id;
$$;

-- Элементы корзины (имя, кол-во, цена за позицию)
CREATE OR REPLACE FUNCTION get_cart_items()
RETURNS TABLE(product_name text, qty int, price numeric)
LANGUAGE sql STABLE AS $$
    SELECT v.name, c.qty, (v.price * c.qty)
    FROM cart c
    JOIN video_cards v ON v.id = c.product_id
    ORDER BY c.id;
$$;

-- Добавить в корзину
CREATE OR REPLACE FUNCTION add_to_cart(p_product_id bigint, p_qty int DEFAULT 1)
RETURNS void
LANGUAGE plpgsql AS $$
BEGIN
    IF p_qty < 1 THEN p_qty := 1; END IF;
    INSERT INTO cart (product_id, qty)
    VALUES (p_product_id, p_qty);
END;
$$;

-- Очистить корзину
CREATE OR REPLACE FUNCTION clear_cart()
RETURNS void
LANGUAGE sql AS $$
    DELETE FROM cart;
$$;

-- Оформить заказ: создать order из корзины, очистить корзину, вернуть заказ как jsonb
CREATE OR REPLACE FUNCTION checkout()
RETURNS jsonb
LANGUAGE plpgsql AS $$
DECLARE
    oid bigint;
    ototal numeric;
    odate timestamptz;
    items_json jsonb;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM cart LIMIT 1) THEN
        RETURN NULL;
    END IF;
    SELECT COALESCE(SUM(v.price * c.qty), 0) INTO ototal
    FROM cart c JOIN video_cards v ON v.id = c.product_id;
    INSERT INTO orders (total) VALUES (ototal) RETURNING id, created_at INTO oid, odate;
    INSERT INTO order_items (order_id, product_name, qty, price)
    SELECT oid, v.name, c.qty, (v.price * c.qty)
    FROM cart c JOIN video_cards v ON v.id = c.product_id;
    SELECT jsonb_agg(jsonb_build_object('name', product_name, 'qty', qty, 'price', price))
    INTO items_json FROM order_items WHERE order_id = oid;
    DELETE FROM cart;
    RETURN jsonb_build_object(
        'id', oid,
        'items', COALESCE(items_json, '[]'::jsonb),
        'total', ototal,
        'date', odate
    );
END;
$$;

-- Список заказов (каждый заказ — jsonb с id, items, total, date)
CREATE OR REPLACE FUNCTION get_orders()
RETURNS SETOF jsonb
LANGUAGE plpgsql STABLE AS $$
DECLARE
    r RECORD;
    items_json jsonb;
BEGIN
    FOR r IN SELECT o.id, o.total, o.created_at FROM orders o ORDER BY o.id DESC
    LOOP
        SELECT jsonb_agg(jsonb_build_object('name', product_name, 'qty', qty, 'price', price))
        INTO items_json FROM order_items WHERE order_id = r.id;
        RETURN NEXT jsonb_build_object(
            'id', r.id,
            'items', COALESCE(items_json, '[]'::jsonb),
            'total', r.total,
            'date', r.created_at
        );
    END LOOP;
END;
$$;

-- Проверка подключения к БД (для health)
CREATE OR REPLACE FUNCTION db_ping()
RETURNS boolean
LANGUAGE sql AS $$
    SELECT true;
$$;
