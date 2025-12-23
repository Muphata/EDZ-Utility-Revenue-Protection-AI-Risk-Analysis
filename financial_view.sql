CREATE OR REPLACE VIEW view_neighborhood_profitability AS
SELECT 
    g.neighborhood_name,
    COALESCE(SUM(b.amount_usd), 0) AS total_revenue,
    COALESCE(e.total_fuel_maint, 0) AS total_expenses,
    (COALESCE(SUM(b.amount_usd), 0) - COALESCE(e.total_fuel_maint, 0)) AS net_profit
FROM dim_geography g
LEFT JOIN dim_customer c ON g.neighborhood_id = c.neighborhood_id
LEFT JOIN fact_billing b ON c.customer_id = b.customer_id
LEFT JOIN (
    SELECT neighborhood_id, SUM(amount_usd) as total_fuel_maint 
    FROM dim_expenses 
    WHERE category IN ('Fuel/Diesel', 'Maintenance')
    GROUP BY neighborhood_id
) e ON g.neighborhood_id = e.neighborhood_id
GROUP BY g.neighborhood_name, e.total_fuel_maint;