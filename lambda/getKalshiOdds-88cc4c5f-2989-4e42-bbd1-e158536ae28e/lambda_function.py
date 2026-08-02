import json
import datetime
from s3handler import s3handler
from KalshiBase import kalshibase

s3 = s3handler(region="eu-north-1", bucket="kalshitickers-114171680089-eu-north-1-an")

def lambda_handler(event, context):
    kal = kalshibase()
    now = datetime.datetime.now()
    series = event.get("series", "")
    status = event.get("status", "")
    days = event.get("days", 5)
    start_time_offset = event.get("start_timefrom_today", None)
    start_time = (now + datetime.timedelta(days=start_time_offset)).strftime("%Y-%m-%d %H:%M:%S") if start_time_offset is not None else None
    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").isoformat() if start_time else datetime.datetime.now().replace(microsecond=0).isoformat()

    markets = kal.get_markets(series_ticker=series, status=status, days=days, start_time=start_time)
    if markets is not None:
        s3.put_file(body = json.dumps(markets), object_name=f"oddsSnapshot/{series if series else 'default'}/{str(now.strftime('%y'))}/{str(now.strftime('%m'))}/{str(now.strftime("%d"))}/{str(now.time().strftime('%H-%M-%S'))}.json")
        pass
    return {
        'statusCode': 200,
        'body': json.dumps('Succesfully retrieved markets: ' + str(len(markets)))
    }
