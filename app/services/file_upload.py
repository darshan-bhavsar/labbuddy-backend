import boto3
import uuid
from typing import Optional
from fastapi import UploadFile, HTTPException
from botocore.exceptions import ClientError
from ..config import settings


class FileUploadService:
    def __init__(self):
        self.s3_client = None
        if settings.aws_access_key_id and settings.aws_secret_access_key:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=settings.aws_region
            )
    
    def upload_file_to_s3(self, file: UploadFile, folder: str = "reports") -> str:
        """Upload file to S3 and return the file URL."""
        if not self.s3_client:
            raise HTTPException(
                status_code=500,
                detail="S3 configuration not available"
            )
        
        if not settings.aws_bucket_name:
            raise HTTPException(
                status_code=500,
                detail="S3 bucket name not configured"
            )
        
        try:
            # Generate unique filename
            file_extension = file.filename.split('.')[-1] if '.' in file.filename else ''
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            s3_key = f"{folder}/{unique_filename}"
            
            # Upload file to S3
            self.s3_client.upload_fileobj(
                file.file,
                settings.aws_bucket_name,
                s3_key,
                ExtraArgs={
                    'ContentType': file.content_type or 'application/octet-stream'
                }
            )
            
            # Return the S3 URL
            file_url = f"https://{settings.aws_bucket_name}.s3.{settings.aws_region}.amazonaws.com/{s3_key}"
            return file_url
            
        except ClientError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload file to S3: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error during file upload: {str(e)}"
            )
    
    def delete_file_from_s3(self, file_url: str) -> bool:
        """Delete file from S3."""
        if not self.s3_client or not settings.aws_bucket_name:
            return False
        
        try:
            # Extract S3 key from URL
            s3_key = file_url.split(f"{settings.aws_bucket_name}.s3.{settings.aws_region}.amazonaws.com/")[-1]
            
            self.s3_client.delete_object(
                Bucket=settings.aws_bucket_name,
                Key=s3_key
            )
            return True
            
        except ClientError as e:
            print(f"Failed to delete file from S3: {str(e)}")
            return False
        except Exception as e:
            print(f"Unexpected error during file deletion: {str(e)}")
            return False
    
    def get_presigned_url(self, file_url: str, expiration: int = 3600) -> Optional[str]:
        """Generate a presigned URL for file access."""
        if not self.s3_client or not settings.aws_bucket_name:
            return None
        
        try:
            # Extract S3 key from URL
            s3_key = file_url.split(f"{settings.aws_bucket_name}.s3.{settings.aws_region}.amazonaws.com/")[-1]
            
            presigned_url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.aws_bucket_name, 'Key': s3_key},
                ExpiresIn=expiration
            )
            return presigned_url
            
        except ClientError as e:
            print(f"Failed to generate presigned URL: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error generating presigned URL: {str(e)}")
            return None
    
    def validate_file(self, file: UploadFile, max_size_mb: int = 10, allowed_types: list = None) -> bool:
        """Validate uploaded file."""
        if allowed_types is None:
            allowed_types = [
                'application/pdf',
                'image/jpeg',
                'image/png',
                'image/tiff',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            ]
        
        # Check file type
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file.content_type} not allowed. Allowed types: {', '.join(allowed_types)}"
            )
        
        # Check file size (read first chunk to get size)
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        max_size_bytes = max_size_mb * 1024 * 1024
        if file_size > max_size_bytes:
            raise HTTPException(
                status_code=400,
                detail=f"File size {file_size / (1024*1024):.2f}MB exceeds maximum allowed size of {max_size_mb}MB"
            )
        
        return True
