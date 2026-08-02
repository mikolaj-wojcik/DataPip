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

    def download_file(self, object_name, file_name=None, bucket_name = None):
        if file_name is None:
            file_name = object_name
        if bucket_name is None:
            bucket_name = self.default_bucket
        try:
            self.s3_client.download_file(bucket_name, object_name, file_name)
            print(f"Plik {object_name} pobrany z {bucket_name} do {file_name}")
        except ClientError as e:
            print(f"Błąd pobierania: {e}")

    def read_file(self, object_name, bucket_name = None):
        if bucket_name is None:
            bucket_name = self.default_bucket
        try:
            response = self.s3_client.get_object(Bucket=bucket_name, Key=object_name)
            data = response['Body'].read().decode('utf-8')
            print(f"Plik {object_name} odczytany z {bucket_name}")
            return data
        except ClientError as e:
            print(f"Błąd odczytu: {e}")
            return None

    def put_file(self, object_name=None, bucket_name = None, body=None):
        if bucket_name is None:
            bucket_name = self.default_bucket
        
            
        self.s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=body)
      