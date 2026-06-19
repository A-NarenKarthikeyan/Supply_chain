CREATE TABLE ecom_orders (
    type VARCHAR(50),
    days_for_shipping_real INT,
    days_for_shipment_scheduled INT,
    benefit_per_order NUMERIC(10, 2),
    sales_per_customer NUMERIC(10, 2),
    delivery_status VARCHAR(50),
    late_delivery_risk INT,
    category_id INT,
    category_name VARCHAR(100),
    customer_city VARCHAR(100),
    customer_country VARCHAR(100),
    customer_email VARCHAR(255),
    customer_fname VARCHAR(100),
    customer_id INT,
    customer_lname VARCHAR(100),
    customer_password VARCHAR(255),
    customer_segment VARCHAR(50),
    customer_state VARCHAR(50),
    customer_street VARCHAR(255),
    customer_zipcode VARCHAR(20), -- Changed to VARCHAR since zip codes have leading zeros
    department_id INT,
    department_name VARCHAR(100),
    latitude NUMERIC(9, 6),
    longitude NUMERIC(9, 6),
    market VARCHAR(50),
    order_city VARCHAR(100),
    order_country VARCHAR(100),
    order_customer_id INT,
    order_date_dateorders VARCHAR(50), -- Raw string timestamp from original dataset
    order_id INT,
    order_item_cardprod_id INT,
    order_item_discount NUMERIC(10, 2),
    order_item_discount_rate NUMERIC(5, 4),
	order_item_id INT,
    order_item_product_price NUMERIC(10, 2),
    order_item_profit_ratio NUMERIC(5, 4),
    order_item_quantity INT,
    sales NUMERIC(10, 2),
    order_item_total NUMERIC(10, 2),
    order_profit_per_order NUMERIC(10, 2),
    order_region VARCHAR(100),
    order_state VARCHAR(100),
    order_status VARCHAR(50),
    order_zipcode VARCHAR(20), -- Changed to VARCHAR to preserve leading zeros
    product_card_id INT,
    product_category_id INT,
    product_description TEXT, -- Changed from float to TEXT as descriptions are strings
    product_image TEXT, -- Changed to TEXT to accommodate long URL strings
    product_name VARCHAR(255),
    product_price NUMERIC(10, 2),
    product_status INT,
    shipping_date_dateorders VARCHAR(50), -- Raw string timestamp from original dataset
    shipping_mode VARCHAR(50),
    order_date TIMESTAMP, -- Maps perfectly to datetime64[ns]
    ship_date TIMESTAMP, -- Maps perfectly to datetime64[ns]
    delay_days NUMERIC, -- Changed to INT as days are discrete units
    delay_cost NUMERIC(10, 2),
    is_delayed SMALLINT -- Optimized for binary 0/1 flags
);


SELECT 
    order_region,
    COUNT(*) AS total_orders,
    SUM(is_delayed::int) AS delayed_orders,
    ROUND(AVG(is_delayed) * 100, 2) AS delay_rate_pct,
    ROUND(AVG(delay_days)::numeric, 3) AS avg_delay_days,
    ROUND(STDDEV(delay_days)::numeric, 3) AS stddev_delay_days
FROM ecom_orders
GROUP BY order_region
ORDER BY delay_rate_pct DESC;


SELECT
    shipping_mode,
    COUNT(*) AS total_orders,
    SUM(is_delayed::int) AS delayed_orders,
    ROUND(AVG(is_delayed) * 100, 2) AS delay_rate_pct,
    ROUND((1 - AVG(is_delayed)) * 100, 2) AS sla_compliance_pct,
    ROUND(AVG(delay_days)::numeric, 3) AS avg_delay_days
FROM ecom_orders
GROUP BY shipping_mode
ORDER BY sla_compliance_pct DESC;

SELECT
    category_name,
    COUNT(*) AS total_orders,
    ROUND(AVG(is_delayed) * 100, 2) AS delay_rate_pct,
    ROUND(AVG(delay_days)::numeric, 3) AS avg_delay_days
FROM ecom_orders
GROUP BY category_name
ORDER BY delay_rate_pct DESC
LIMIT 15;

SELECT
    order_region,
    shipping_mode,
    COUNT(*) AS total_orders,
    ROUND(AVG(is_delayed) * 100, 2) AS delay_rate_pct,
    ROUND(AVG(delay_days)::numeric, 3) AS avg_delay_days,
    ROUND(SUM(delay_cost)::numeric, 2) AS total_delay_cost
FROM ecom_orders
GROUP BY order_region, shipping_mode
HAVING COUNT(*) > 100
ORDER BY delay_rate_pct DESC
LIMIT 10;

SELECT 
    shipping_mode,
    COUNT(*) AS total_orders,
    ROUND(SUM(delay_cost)::numeric, 2) AS total_delay_cost,
    ROUND(AVG(delay_cost)::numeric, 2) AS avg_cost_per_order
FROM ecom_orders
WHERE shipping_mode = 'First Class'
AND delay_cost IS NOT NULL
GROUP BY shipping_mode;

SELECT 
    order_region,
    shipping_mode,
    COUNT(*) AS total_orders,
    ROUND(AVG(is_delayed) * 100, 2) AS delay_rate_pct,
    ROUND(AVG(delay_days)::numeric, 3) AS avg_delay_days,
    ROUND(SUM(delay_cost)::numeric, 2) AS total_delay_cost
FROM ecom_orders
WHERE shipping_mode != 'First Class'
GROUP BY order_region, shipping_mode
HAVING COUNT(*) > 100
ORDER BY delay_rate_pct DESC
LIMIT 10;

SELECT
    order_region,
    COUNT(*) AS total_orders,
    SUM(is_delayed::int) AS delayed_orders,
    ROUND(SUM(delay_cost)::numeric, 2) AS total_delay_cost,
    ROUND(AVG(delay_cost)::numeric, 2) AS avg_delay_cost_per_order
FROM ecom_orders
WHERE delay_cost IS NOT NULL
GROUP BY order_region
ORDER BY total_delay_cost DESC;

SELECT
    ROUND(SUM(delay_cost)::numeric, 2) AS grand_total_delay_cost,
    COUNT(*) AS total_orders_with_cost,
    ROUND(AVG(delay_cost)::numeric, 2) AS global_avg_cost_per_order
FROM ecom_orders
WHERE delay_cost IS NOT NULL;

