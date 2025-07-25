import boto3
from botocore.config import Config
from app.core.config import settings

class CloudflareR2Client:
    def __init__(self):
        self.client = boto3.client(
            's3',
            endpoint_url=settings.CLOUDFLARE_R2_ENDPOINT,
            aws_access_key_id=settings.CLOUDFLARE_R2_ACCESS_KEY,
            aws_secret_access_key=settings.CLOUDFLARE_R2_SECRET_KEY,
            config=Config(signature_version='s3v4'),
            region_name='auto'
        )
        self.bucket = settings.CLOUDFLARE_R2_BUCKET
    
    def upload_file(self, file_data: bytes, key: str, content_type: str = 'image/jpeg') -> str:
        """Upload file to Cloudflare R2 and return public URL"""
        self.client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=file_data,
            ContentType=content_type
        )
        return f"https://{self.bucket}.{settings.CLOUDFLARE_ACCOUNT_ID}.r2.cloudflarestorage.com/{key}"

r2_client = CloudflareR2Client()
