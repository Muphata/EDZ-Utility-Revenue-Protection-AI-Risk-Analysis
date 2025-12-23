CREATE OR REPLACE VIEW view_customer_analytics AS
SELECT 
    c.customer_id,
    c.neighborhood_id,
    g.neighborhood_name,
    g.assigned_collector_id AS staff_id, -- Added from your discovery
    c.max_amperage,
    c.connection_type,
    r.kwh_value,
    b.amount_usd, 
    b.status AS payment_status,
    -- Keeps your original GPS logic
    ST_Distance_Sphere(
        point(c.customer_long, c.customer_lat),
        point(r.captured_long, r.captured_lat)
    ) AS reader_distance_meters,
    -- Label for AI/Operational Audit
    CASE WHEN b.status = 'Unpaid' THEN 1 ELSE 0 END AS is_late_payer
FROM dim_customer c
JOIN dim_geography g ON c.neighborhood_id = g.neighborhood_id
JOIN fact_readings r ON c.customer_id = r.customer_id
JOIN fact_billing b ON r.reading_id = b.reading_id
WHERE c.is_active = 1; -- Keeps your filter for active customers