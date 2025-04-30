SELECT
  time,
  CASE WHEN qty > 0 THEN price END AS buys,
  CASE WHEN qty < 0 THEN price END AS sells
FROM public.trades
