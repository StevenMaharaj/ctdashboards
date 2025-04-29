SELECT 
    time,
    price,
    qty,
    SUM(qty) OVER (ORDER BY time) AS pos
FROM 
    public.trades
-- LIMIT 10;