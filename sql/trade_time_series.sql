SELECT
  time,
  CASE WHEN qty > 0 THEN price END AS price_up,
  CASE WHEN qty < 0 THEN price END AS price_down
FROM public.trades
