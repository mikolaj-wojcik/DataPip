
with source as (

    select * from {{ source('raw', 'market_snapshots') }}

),

	renamed as (

		select
		timestamp as snapshot_time,
		event_ticker,
		ticker,
		title,
		yes_sub_title,
		status,
		close_time,
		last_price_dollars as last_price,
		yes_bid_dollars as yes_bid,
		yes_ask_dollars as yes_ask,
		no_bid_dollars as no_bid,
		no_ask_dollars as no_ask,
		yes_bid_size_fp,
		yes_ask_size_fp,
		volume_fp,
		open_interest_fp,
		created_at
		from source

	),

    key_added as (
        select
        md5(ticker || '|' || snapshot_time::text) as snapshot_id,
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
		created_at
        from renamed
            )

	select * from key_added