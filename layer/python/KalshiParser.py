
def parse_to_json(data, sport=None, market=None):
    """
    Parses the given data to JSON format.

    Args:
        data (str): The data to be parsed.

    Returns:
        dict: The parsed JSON data.
    """
    import json
    try:
        useful_data =[]
        market_list = json.loads(data)
        for match in market_list:
            match_dict = {}
            
            if match['open_interest_fp'] == '0.0000' or match['status'] == 'finalized':
                continue

            market_dict = {
                'event_ticker': match.get('event_ticker'),
                'close_time': match.get('close_time'),
                'last_price_dollars': match.get('last_price_dollars'),
                'no_ask_dollars': match.get('no_ask_dollars'),
                'no_bid_dollars': match.get('no_bid_dollars'),
                'open_interest_fp': match.get('open_interest_fp'),
                'ticker': match.get('ticker'),
                'title': match.get('title'),
                'volune_fp': match.get('volune_fp'),
                'yes_ask_dollars': match.get('yes_ask_dollars'),
                'yes_ask_size_fp': match.get('yes_ask_size_fp'),
                'yes_bid_dollars': match.get('yes_bid_dollars'),
                'yes_bid_size_fp': match.get('yes_bid_size_fp'),
                'yes_sub_title': match.get('yes_sub_title'),
            }
            useful_data.append(market_dict)
        return useful_data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        raise
        return None