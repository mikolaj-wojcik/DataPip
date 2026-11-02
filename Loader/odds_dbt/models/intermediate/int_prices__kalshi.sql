with prices as (

    select * from {{ ref('stg_kalshi__snapshots') }}

)

select
        snapshot_id,
        snapshot_time,
        event_ticker,
		ticker,
		title,
		yes_sub_title,
		status,
		close_time,
		last_price,
		yes_bid,
		yes_ask,
		no_bid,
		no_ask,
		yes_bid_size_fp,
		yes_ask_size_fp,
		volume_fp,
		open_interest_fp,
		created_at,
		yes_bid_size_fp > 0 as has_bid,
        yes_ask_size_fp > 0 as has_ask,
        case when yes_bid_size_fp > 0 and yes_ask_size_fp > 0
             then yes_ask - yes_bid end as spread,
        case when yes_bid_size_fp > 0 and yes_ask_size_fp > 0
             then (yes_bid + yes_ask) / 2 end as mid_price
from prices