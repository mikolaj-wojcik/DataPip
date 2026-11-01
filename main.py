
import requests
import json
import boto3

ssm = boto3.client("ssm", region_name="eu-north-1")

def refresh_tickers(tag='Soccer'):
    url = "https://external-api.kalshi.com/trade-api/v2/series?category=Sports&tags=Soccer&include_product_metadata=true&include_volume=true"
    r = requests.get(url)

    dict = {}
    if r.status_code == 200:
        jsonObj = json.loads(r.text)
        for item in jsonObj['series']:
            if tag in item['tags']:
                if 'GAME' in item['ticker'] or 'TOTAL' in item['ticker'] or 'SPREAD' in item['ticker'] or 'BTTS' in item['ticker'] or 'ADVANCE' in item['ticker']:
                    dict[item['ticker'][2:5] +' '+ item['title']] = item['ticker']
        pass
    return dict
    pass

def lambda_handler(event, context):
    tag = event.get('tag')

    dict1 = refresh_tickers(tag)

    if dict1 != {}:
        response = ssm.put_parameter(
            Name="/kalshi/dev/"+ tag,
            Value=json.dumps(dict1),
            Type="String",
            Overwrite=True,
        )
    pass


