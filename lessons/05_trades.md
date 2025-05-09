
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

## Separate Buy and Sell
We will separate the trade into 2 series. Buy trades and Sell trades. Then plot both of them together. Buys will be colored green and sells.

```sql
SELECT
  time,
  CASE WHEN qty > 0 THEN price END AS buys,
  CASE WHEN qty < 0 THEN price END AS sells
FROM public.trades
```
## Summary for trades
```sql
SELECT
        SUM(ABS(qty)) as total_traded,
        Count(id) as n_trades,
        COUNT(*) FILTER (WHERE qty > 0)   AS num_buys,
        COUNT(*) FILTER (WHERE qty < 0)   AS num_sells
    FROM 
        public.trades
```