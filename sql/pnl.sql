WITH trade_data AS (
    SELECT 
        time,
        price,
        qty,
        SUM(qty) OVER (ORDER BY time) AS cum_pos,
        SUM(qty * price) OVER (ORDER BY time) AS cum_value
    FROM 
        public.trades
),
pnl_data AS (
    SELECT 
        time,
        price,
        qty,
        cum_pos,
        LAG(cum_pos) OVER (ORDER BY time) AS prev_cum_pos,
        CASE 
            WHEN cum_pos = 0 THEN cum_value
            ELSE 0
        END AS realized_pnl,
        CASE 
            WHEN cum_pos <> 0 THEN (cum_pos * (price - (cum_value / NULLIF(cum_pos, 0))))
            ELSE 0
        END AS unrealized_pnl
    FROM 
        trade_data
)
SELECT 
    time,
    price,
    qty,
    cum_pos,
    realized_pnl,
    unrealized_pnl
FROM 
    pnl_data
ORDER BY 
    time;