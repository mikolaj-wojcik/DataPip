import json
import urllib.request
import boto3

s3 = boto3.client("s3")
BUCKET_NAME = "kalshitickers-114171680089-eu-north-1-an"

def refresh_tickers(tag='Soccer'):
    url = "https://external-api.kalshi.com/trade-api/v2/series?category=Sports&tags=Soccer&include_product_metadata=true&include_volume=true"

    r = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0"}
    )  # Nagłówek dla bezpieczeństwa

    dict = {}
    try:
        with urllib.request.urlopen(r, timeout=10) as response:
            if response.status == 200:
                jsonObj = json.loads(response.read().decode("utf-8"))
                for item in jsonObj['series']:
                    if tag in item['tags']:
                        if 'GAME' in item['ticker'] or 'TOTAL' in item['ticker'] or 'SPREAD' in item['ticker'] or 'BTTS' in item['ticker'] or 'ADVANCE' in item['ticker']:
                            dict[item['ticker'][2:5] +' '+ item['title']] = item['ticker']
                pass

    except Exception as e:
        print(e)
        pass
    return dict



def lambda_handler(event, context):
    tag = event.get('tag')
    dict1 = refresh_tickers(tag)
    if dict1 != {}:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=f"kalshi/{tag}.json",
            Body=json.dumps(dict1),
            ContentType="application/json",
        )
    return {
        'statusCode': 200,
        'body': json.dumps('Tickers refreshed')
    }
