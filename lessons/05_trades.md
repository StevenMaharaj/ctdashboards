
## Calculate Position
Assuming we're starting with a 0 position the running position is just going to be the cumulative sum of the trade quantities.

```sql
SELECT 
    time,
    price,
    qty,
    SUM(qty) OVER (ORDER BY time) AS pos
FROM 
    public.trades
-- LIMIT 10;
```



To calculate cumulative position (CUMSUM of qty), realized PnL, and unrealized PnL, you can use SQL window functions. Here's how you can structure the query:

Assumptions:
Realized PnL: Calculated when a position is closed (e.g., when the cumulative position returns to zero or decreases).
Unrealized PnL: Calculated based on the current cumulative position and the difference between the current price and the average entry price.

To calculate **cumulative position (CUMSUM of `qty`)**, **realized PnL**, and **unrealized PnL**, you can use SQL window functions. Here's how you can structure the query:

### Assumptions:
1. **Realized PnL**: Calculated when a position is closed (e.g., when the cumulative position returns to zero or decreases).
2. **Unrealized PnL**: Calculated based on the current cumulative position and the difference between the current price and the average entry price.

### Query:
```sql
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
```

### Explanation:
1. **`trade_data` CTE**:
   - Calculates the cumulative position (`cum_pos`) using `SUM(qty) OVER (ORDER BY time)`.
   - Calculates the cumulative value (`cum_value`) as the running total of `qty * price`.

2. **`pnl_data` CTE**:
   - **Realized PnL**:
     - Realized PnL is calculated when the cumulative position (`cum_pos`) returns to zero.
     - Uses a `CASE` statement to assign the cumulative value (`cum_value`) as realized PnL when `cum_pos = 0`.
   - **Unrealized PnL**:
     - Unrealized PnL is calculated as the difference between the current price and the average entry price (`cum_value / cum_pos`), multiplied by the current cumulative position.

3. **Final SELECT**:
   - Outputs the `time`, `price`, `qty`, `cum_pos`, `realized_pnl`, and `unrealized_pnl`.

### Notes:
- Replace `public.trades` with your actual table name.
- The `NULLIF(cum_pos, 0)` prevents division by zero when calculating the average entry price.
- This query assumes that `time` is the column used to order trades chronologically. Adjust as needed for your schema.To calculate **cumulative position (CUMSUM of `qty`)**, **realized PnL**, and **unrealized PnL**, you can use SQL window functions. Here's how you can structure the query:

### Assumptions:
1. **Realized PnL**: Calculated when a position is closed (e.g., when the cumulative position returns to zero or decreases).
2. **Unrealized PnL**: Calculated based on the current cumulative position and the difference between the current price and the average entry price.

### Query:
```sql
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
```

### Explanation:
1. **`trade_data` CTE**:
   - Calculates the cumulative position (`cum_pos`) using `SUM(qty) OVER (ORDER BY time)`.
   - Calculates the cumulative value (`cum_value`) as the running total of `qty * price`.

2. **`pnl_data` CTE**:
   - **Realized PnL**:
     - Realized PnL is calculated when the cumulative position (`cum_pos`) returns to zero.
     - Uses a `CASE` statement to assign the cumulative value (`cum_value`) as realized PnL when `cum_pos = 0`.
   - **Unrealized PnL**:
     - Unrealized PnL is calculated as the difference between the current price and the average entry price (`cum_value / cum_pos`), multiplied by the current cumulative position.

3. **Final SELECT**:
   - Outputs the `time`, `price`, `qty`, `cum_pos`, `realized_pnl`, and `unrealized_pnl`.

### Notes:
- Replace `public.trades` with your actual table name.
- The `NULLIF(cum_pos, 0)` prevents division by zero when calculating the average entry price.
- This query assumes that `time` is the column used to order trades chronologically. Adjust as needed for your schema.