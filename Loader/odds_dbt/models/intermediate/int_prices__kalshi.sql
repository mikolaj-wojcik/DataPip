with prices as (

    select * from {{ ref('stg_kalshi__snapshots') }}

)

select
    event_ticker,
    ticker,
    max(yes_ask) as max_price,
    min(yes_ask) as min_price,
    avg(yes_ask) as avg_price,
    max(volume_fp) as total_volume
from prices where status = 'active' group by 1,2