import boto3
from botocore.exceptions import ClientError


class s3handler():

    def __init__(self, region, bucket = None):
        self.s3_client = boto3.client('s3', region_name = region)
        self.default_bucket = bucket

    def listBuckets(self):
        try:
            response = self.s3_client.list_buckets()
            print("Twoje buckety S3:")
            for bucket in response['Buckets']:
                print(f" - {bucket['Name']}")
        except ClientError as e:
            print(f"Błąd połączenia z S3: {e}")
        pass

    def upload_file(self, file_name, object_name=None, bucket_name = None):
        if object_name is None:
            object_name = file_name
        if bucket_name is None:
            bucket_name = self.default_bucket
        try:
            self.s3_client.upload_file(file_name, bucket_name, object_name)
            print(f"Plik {file_name} wysłany do {bucket_name}/{object_name}")
        except ClientError as e:
            print(f"Błąd wysyłania: {e}")