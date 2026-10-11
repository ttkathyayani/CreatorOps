import os
import mimetypes
from django.conf import settings
import boto3
from botocore.exceptions import ClientError


class CloudMediaStorage:
    """
    Unified storage handler supporting AWS S3 with presigned URLs
    and seamless local file storage fallback.
    """
    def __init__(self):
        self.use_s3 = getattr(settings, "USE_S3", False)
        self.bucket_name = getattr(settings, "AWS_STORAGE_BUCKET_NAME", "")
        self.region = getattr(settings, "AWS_S3_REGION_NAME", "ap-south-1")
        self._s3_client = None

        if self.use_s3 and self.bucket_name:
            try:
                self._s3_client = boto3.client(
                    "s3",
                    region_name=self.region,
                    aws_access_key_id=getattr(settings, "AWS_ACCESS_KEY_ID", None) or None,
                    aws_secret_access_key=getattr(settings, "AWS_SECRET_ACCESS_KEY", None) or None,
                )
            except Exception:
                self._s3_client = None

    def upload_file(self, file_obj, object_key):
        """Uploads file to S3 bucket if configured, or returns None."""
        if self._s3_client and self.bucket_name:
            try:
                mime_type, _ = mimetypes.guess_type(file_obj.name)
                extra_args = {"ContentType": mime_type or "application/octet-stream"}
                self._s3_client.upload_fileobj(
                    file_obj,
                    self.bucket_name,
                    object_key,
                    ExtraArgs=extra_args
                )
                return object_key
            except ClientError as e:
                print(f"[AWS S3 Warning] Upload failed: {e}")
                return None
        return None

    def get_presigned_url(self, object_key, expires_in=3600):
        """Generate a time-limited secure presigned URL for private S3 assets."""
        if self._s3_client and self.bucket_name and object_key:
            try:
                return self._s3_client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": self.bucket_name, "Key": object_key},
                    ExpiresIn=expires_in,
                )
            except ClientError as e:
                print(f"[AWS S3 Warning] Presigned URL failed: {e}")
                return None
        return None


cloud_storage = CloudMediaStorage()
