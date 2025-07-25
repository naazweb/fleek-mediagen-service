import boto3
from botocore.config import Config
from app.core.config import settings

class CloudflareR2Client:
    """
    Client for uploading files to Cloudflare R2 storage.
    
    Uses boto3 S3-compatible API to interact with Cloudflare R2.
    Configured with R2 endpoint, credentials, and bucket from settings.
    """
    
    def __init__(self):
        """
        Initialize Cloudflare R2 client with boto3 S3 client.
        
        Configures client with:
        - R2 endpoint URL
        - Access key and secret key
        - S3v4 signature version
        - Auto region for R2 compatibility
        """
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
        """
        Upload file to Cloudflare R2 storage and return public URL.
        
        Args:
            file_data (bytes): Raw file data to upload
            key (str): Object key/path in the bucket (e.g., "images/photo.jpg")
            content_type (str): MIME type of the file (default: 'image/jpeg')
        
        Returns:
            str: Public URL where the uploaded file can be accessed
        
        Raises:
            ClientError: If upload fails due to invalid credentials, bucket, etc.
        """
        self.client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=file_data,
            ContentType=content_type
        )
        return f"{settings.CLOUDFLARE_R2_PUBLIC_URL}/{key}"

r2_client = CloudflareR2Client()
