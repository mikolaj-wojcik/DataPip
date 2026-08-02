from datetime import datetime, timedelta

from KalshiParser import parse_to_json
import json

class kalshibase:
    def __init__(self):
        self.api_key = None
        self.get_markets_endpoint = "https://external-api.kalshi.com/trade-api/v2/markets"

        pass


    def get_markets(self, series_ticker = None, status = None, days = None, start_time = None):
        """
        Retrieves markets from the Kalshi API based on the provided series ticker and status.

        Args:
            series_ticker (str, optional): The series ticker to filter markets. Defaults to None.
            status (str, optional): The status to filter markets. Defaults to None.
            days (int, optional): The number of days to filter markets. Defaults to None.
            start_time (datetime, optional): The start time to filter markets. Defaults to None.

        Returns:
            dict: A dictionary containing the retrieved markets data.
        """
        import requests

        headers = {
            "accept": "application/json",
            "X-API-Key": self.api_key
        }

        
        params= {
           "cursor" : "",
            "series_ticker": series_ticker or "" ,
            "max_close_ts": int(((datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S") if start_time else datetime.now()) + timedelta(days=days)).timestamp()) or None,
            "status": status or "",
            "min_close_ts": int(datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S").timestamp()) if start_time else None
        }
        resp_cursor = 'a'
        whole_resp = []
        counter = 0
        while resp_cursor != '':

            response = requests.get(self.get_markets_endpoint, headers=headers, params=params)
            if len(whole_resp) > 1000:
                print(f"Counter: {counter}, Retrieved {len(whole_resp)} markets from Kalshi API.")
                #whole_resp = []
            if response.status_code == 200:
                resp = response.json()
                resp_cursor = resp.get('cursor', '')
                params['cursor'] = resp_cursor
                whole_resp += parse_to_json(json.dumps(resp.get('markets', '')))
                
                counter += 100
            else:
                if response.status_code == 429:
                    print("Cooldown in effect. Waiting for 1 seconds before retrying...")
                    import time
                    time.sleep(1)
                else:
                    print(f"Error: {response.status_code} - {response.text}")
                    raise Exception(f"Error: {response.status_code} - {response.text}")
        print(f"Retrieved {len(whole_resp)} markets from Kalshi API.")
        return whole_resp
