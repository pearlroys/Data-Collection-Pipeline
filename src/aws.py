import boto3
import botocore
import pandas as pd
# import sqlalchemy


from uuid import uuid4
BUCKET_NAME = 'medexpress-bucket'

class AwsScraper:
    def __init__(self):
        self.data_store = "./raw_data"

   
    def upload_file_method(self, file_name) -> str:
        """Function takes in an existing file and saves it to the names bucket in S3 with the specified name.
        Args:
            file_name (str): Name of file to be uploaded to S3.
            object_name (str): Desired name of file when saved in S3.
        Returns:
            str: URL of file in S3.
        """
        s3_client = boto3.client('s3')
        
        try:
            s3_client.get_object(bucket=BUCKET_NAME, Key=file_name)
            
        except:
            s3_client.upload_file(f"raw_data/{file_name}/data.json", BUCKET_NAME, file_name)

        file_url = f's3://{BUCKET_NAME}/{file_name}'
        
        return file_url

    def upload_image_method(self, file_name) -> str:
        """Function takes in an existing file and saves it to the names bucket in S3 with the specified name.
        Args:
            file_name (str): Name of file to be uploaded to S3.
            object_name (str): Desired name of file when saved in S3.
        Returns:
            str: URL of file in S3.
        """
        s3_client = boto3.client('s3')
        
        try:
            s3_client.get_object(bucket=BUCKET_NAME, Key=file_name)
            
        except:
            s3_client.upload_file(f"raw_data/images/{file_name}.jpg", BUCKET_NAME, file_name)

        file_url = f's3://{BUCKET_NAME}/{file_name}'
        
        return file_url


aws = AwsScraper()
# aws.upload_file_method('asthma')