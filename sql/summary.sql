SELECT
        SUM(ABS(qty)) as total_traded,
        Count(id) as n_trades,
        COUNT(*) FILTER (WHERE qty > 0)   AS num_buys,
        COUNT(*) FILTER (WHERE qty < 0)   AS num_sells
    FROM 
        public.trades