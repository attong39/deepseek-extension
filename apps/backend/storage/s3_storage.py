"""S3-compatible storage for ZETA AI Server.





This module provides S3-compatible cloud storage functionality including:


- AWS S3 integration


- MinIO support for self-hosted S3


- Bucket management


- Object upload/download with multipart support


- Presigned URL generation


- Metadata and tagging support


"""

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
import Exception
import ImportError
import ValueError
import access_key
import bool
import dest_key
import dict
import e
import endpoint_url
import etag
import expiration
import f
import http_method
import int
import k
import key
import last_modified
import len
import list
import max_age_days
import max_concurrency
import max_keys
import metadata
import multipart_chunksize
import multipart_threshold
import obj
import open
import page
import prefix
import region
import secret_key
import self
import size
import source_key
import storage_class
import str
import sum
import tag
import tuple
import upload_args
import use_ssl
import v

logger = logging.getLogger(__name__)


class S3Config:
    """Configuration for S3 storage."""

    def __init__(
        self,
        endpoint_url: str | None = None,
        access_key: str | None = None,
        secret_key: str | None = None,
        region: str = "us-east-1",
        bucket_name: str = "zeta-ai-storage",
        use_ssl: bool = True,
        multipart_threshold: int = 64 * 1024 * 1024,  # 64MB
        multipart_chunksize: int = 16 * 1024 * 1024,  # 16MB
        max_concurrency: int = 10,
    ):
        """Initialize S3 configuration.





        Args:


            endpoint_url: S3 endpoint URL (None for AWS S3)


            access_key: S3 access key


            secret_key: S3 secret key


            region: AWS region


            bucket_name: S3 bucket name


            use_ssl: Whether to use SSL


            multipart_threshold: Threshold for multipart uploads


            multipart_chunksize: Chunk size for multipart uploads


            max_concurrency: Maximum concurrent uploads


        """

        self.endpoint_url = endpoint_url

        self.access_key = access_key

        self.secret_key = secret_key

        self.region = region

        self.bucket_name = bucket_name

        self.use_ssl = use_ssl

        self.multipart_threshold = multipart_threshold

        self.multipart_chunksize = multipart_chunksize

        self.max_concurrency = max_concurrency


class S3Object:
    """Represents an S3 object."""

    def __init__(
        self,
        key: str,
        size: int,
        last_modified: datetime,
        etag: str,
        storage_class: str = "STANDARD",
        metadata: dict[str, str] | None = None,
        tags: dict[str, str] | None = None,
    ):
        """Initialize S3 object.





        Args:


            key: Object key/path


            size: Object size in bytes


            last_modified: Last modification timestamp


            etag: Object ETag


            storage_class: Storage class


            metadata: Object metadata


            tags: Object tags


        """

        self.key = key

        self.size = size

        self.last_modified = last_modified

        self.etag = etag

        self.storage_class = storage_class

        self.metadata = metadata or {}

        self.tags = tags or {}

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""

        return {
            "key": self.key,
            "size": self.size,
            "last_modified": self.last_modified.isoformat(),
            "etag": self.etag,
            "storage_class": self.storage_class,
            "metadata": self.metadata,
            "tags": self.tags,
        }


class S3Storage:
    """S3-compatible storage manager."""

    def __init__(self, config: S3Config):
        """Initialize S3 storage.





        Args:


            config: S3 configuration


        """

        self.config = config

        self._client = None

        self.__ = None

    def _get_client(self):
        """Get or create S3 client."""

        if self._client is None:
            try:
                import boto3
                from botocore.config import Config

                # Create session

                self.__ = boto3.Session(
                    aws_access_key_id=self.config.access_key,
                    aws_secret_access_key=self.config.secret_key,
                    region_name=self.config.region,
                )

                # Create client with configuration

                client_config = Config(
                    region_name=self.config.region,
                    retries={"max_attempts": 3},
                    max_pool_connections=self.config.max_concurrency,
                )

                self._client = self._session.client(
                    "s3",
                    endpoint_url=self.config.endpoint_url,
                    config=client_config,
                    use_ssl=self.config.use_ssl,
                )

            except ImportError:
                raise ImportError(
                    "boto3 is required for S3 storage. Install with: pip install boto3"
                )

        return self._client

    def create_bucket(self, bucket_name: str | None = None) -> bool:
        """Create S3 bucket.





        Args:


            bucket_name: Bucket name (uses default if None)





        Returns:


            True if successful, False otherwise


        """

        bucket_name = bucket_name or self.config.bucket_name

        try:
            client = self._get_client()

            # Check if bucket already exists

            try:
                client.head_bucket(Bucket=bucket_name)

                logger.info(f"Bucket already exists: {bucket_name}")

                return True

            except client.exceptions.NoSuchBucket:
                pass

            # Create bucket

            if self.config.region == "us-east-1":
                # us-east-1 doesn't need LocationConstraint

                client.create_bucket(Bucket=bucket_name)

            else:
                client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={
                        "LocationConstraint": self.config.region
                    },
                )

            logger.info(f"Created bucket: {bucket_name}")

            return True

        except Exception as e:
            logger.error(f"Failed to create bucket {bucket_name}: {e}")

            return False

    def bucket_exists(self, bucket_name: str | None = None) -> bool:
        """Check if bucket exists.





        Args:


            bucket_name: Bucket name (uses default if None)





        Returns:


            True if bucket exists, False otherwise


        """

        bucket_name = bucket_name or self.config.bucket_name

        try:
            client = self._get_client()

            client.head_bucket(Bucket=bucket_name)

            return True

        except Exception:
            return False

    def upload_file(
        self,
        local_path: str | Path,
        key: str,
        metadata: dict[str, str] | None = None,
        tags: dict[str, str] | None = None,
        storage_class: str = "STANDARD",
    ) -> S3Object | None:
        """Upload file to S3.





        Args:


            local_path: Local file path


            key: S3 object key


            metadata: Object metadata


            tags: Object tags


            storage_class: Storage class





        Returns:


            S3Object if successful, None otherwise


        """

        try:
            local_path = Path(local_path)

            if not local_path.exists():
                logger.error(f"File not found: {local_path}")

                return None

            client = self._get_client()

            # Prepare upload arguments

            upload_args: dict[str, Any] = {"StorageClass": storage_class}

            if metadata:
                upload_args["Metadata"] = metadata

            # Upload file

            file_size = local_path.stat().st_size

            if file_size >= self.config.multipart_threshold:
                # Use multipart upload for large files

                self._multipart_upload(client, local_path, key, upload_args)

            else:
                # Use simple upload for small files

                with open(local_path, "rb") as f:
                    client.upload_fileobj(
                        f, self.config.bucket_name, key, ExtraArgs=upload_args
                    )

            # Add tags if provided

            if tags:
                self.put_object_tags(key, tags)

            # Get object info

            return self.get_object_info(key)

        except Exception as e:
            logger.error(f"Failed to upload file {local_path} to {key}: {e}")

            return None

    def _multipart_upload(
        self, client, local_path: Path, key: str, upload_args: dict[str, Any]
    ) -> None:
        """Perform multipart upload."""

        # Start multipart upload

        response = client.create_multipart_upload(
            Bucket=self.config.bucket_name, Key=key, **upload_args
        )

        upload_id = response["UploadId"]

        try:
            parts = []

            part_number = 1

            with open(local_path, "rb") as f:
                while True:
                    chunk = f.read(self.config.multipart_chunksize)

                    if not chunk:
                        break

                    # Upload part

                    part_response = client.upload_part(
                        Bucket=self.config.bucket_name,
                        Key=key,
                        PartNumber=part_number,
                        UploadId=upload_id,
                        Body=chunk,
                    )

                    parts.append(
                        {"ETag": part_response["ETag"], "PartNumber": part_number}
                    )

                    part_number += 1

            # Complete multipart upload

            client.complete_multipart_upload(
                Bucket=self.config.bucket_name,
                Key=key,
                UploadId=upload_id,
                MultipartUpload={"Parts": parts},
            )

        except Exception as e:
            # Abort multipart upload on error

            client.abort_multipart_upload(
                Bucket=self.config.bucket_name, Key=key, UploadId=upload_id
            )

            raise e

    def download_file(self, key: str, local_path: str | Path) -> bool:
        """Download file from S3.





        Args:


            key: S3 object key


            local_path: Local file path to save to





        Returns:


            True if successful, False otherwise


        """

        try:
            local_path = Path(local_path)

            local_path.parent.mkdir(parents=True, exist_ok=True)

            client = self._get_client()

            with open(local_path, "wb") as f:
                client.download_fileobj(self.config.bucket_name, key, f)

            logger.info(f"Downloaded {key} to {local_path}")

            return True

        except Exception as e:
            logger.error(f"Failed to download {key} to {local_path}: {e}")

            return False

    def delete_object(self, key: str) -> bool:
        """Delete object from S3.





        Args:


            key: S3 object key





        Returns:


            True if successful, False otherwise


        """

        try:
            client = self._get_client()

            client.delete_object(Bucket=self.config.bucket_name, Key=key)

            logger.info(f"Deleted object: {key}")

            return True

        except Exception as e:
            logger.error(f"Failed to delete object {key}: {e}")

            return False

    def get_object_info(self, key: str) -> S3Object | None:
        """Get object information.





        Args:


            key: S3 object key





        Returns:


            S3Object if found, None otherwise


        """

        try:
            client = self._get_client()

            # Get object metadata

            response = client.head_object(Bucket=self.config.bucket_name, Key=key)

            # Get object tags

            try:
                tags_response = client.get_object_tagging(
                    Bucket=self.config.bucket_name, Key=key
                )

                tags = {
                    tag["Key"]: tag["Value"] for tag in tags_response.get("TagSet", [])
                }

            except Exception:
                tags = {}

            return S3Object(
                key=key,
                size=response["ContentLength"],
                last_modified=response["LastModified"],
                etag=response["ETag"].strip('"'),
                storage_class=response.get("StorageClass", "STANDARD"),
                metadata=response.get("Metadata", {}),
                tags=tags,
            )

        except Exception as e:
            logger.error(f"Failed to get object info for {key}: {e}")

            return None

    def list_objects(
        self, prefix: str = "", max_keys: int | None = None
    ) -> list[S3Object]:
        """List objects in bucket.





        Args:


            prefix: Object key prefix filter


            max_keys: Maximum number of objects to return





        Returns:


            List of S3Object instances


        """

        objects = []

        try:
            client = self._get_client()

            paginator = client.get_paginator("list_objects_v2")

            page_iterator = paginator.paginate(
                Bucket=self.config.bucket_name,
                Prefix=prefix,
                PaginationConfig={"MaxItems": max_keys} if max_keys else {},
            )

            for page in page_iterator:
                for obj in page.get("Contents", []):
                    s3_object = S3Object(
                        key=obj["Key"],
                        size=obj["Size"],
                        last_modified=obj["LastModified"],
                        etag=obj["ETag"].strip('"'),
                        storage_class=obj.get("StorageClass", "STANDARD"),
                    )

                    objects.append(s3_object)

        except Exception as e:
            logger.error(f"Failed to list objects: {e}")

        return objects

    def generate_presigned_url(
        self, key: str, expiration: int = 3600, http_method: str = "GET"
    ) -> str | None:
        """Generate presigned URL for object access.





        Args:


            key: S3 object key


            expiration: URL expiration time in seconds


            http_method: HTTP method (GET, PUT, etc.)





        Returns:


            Presigned URL if successful, None otherwise


        """

        try:
            client = self._get_client()

            if http_method.upper() == "GET":
                method = "get_object"

            elif http_method.upper() == "PUT":
                method = "put_object"

            else:
                raise ValueError(f"Unsupported HTTP method: {http_method}")

            url = client.generate_presigned_url(
                method,
                Params={"Bucket": self.config.bucket_name, "Key": key},
                ExpiresIn=expiration,
            )

            return url

        except Exception as e:
            logger.error(f"Failed to generate presigned URL for {key}: {e}")

            return None

    def put_object_tags(self, key: str, tags: dict[str, str]) -> bool:
        """Add tags to object.





        Args:


            key: S3 object key


            tags: Tags to add





        Returns:


            True if successful, False otherwise


        """

        try:
            client = self._get_client()

            tag_set = [{"Key": k, "Value": v} for k, v in tags.items()]

            client.put_object_tagging(
                Bucket=self.config.bucket_name, Key=key, Tagging={"TagSet": tag_set}
            )

            return True

        except Exception as e:
            logger.error(f"Failed to put tags for {key}: {e}")

            return False

    def copy_object(
        self, source_key: str, dest_key: str, source_bucket: str | None = None
    ) -> bool:
        """Copy object within or between buckets.





        Args:


            source_key: Source object key


            dest_key: Destination object key


            source_bucket: Source bucket (uses default if None)





        Returns:


            True if successful, False otherwise


        """

        try:
            source_bucket = source_bucket or self.config.bucket_name

            client = self._get_client()

            copy_source = {"Bucket": source_bucket, "Key": source_key}

            client.copy_object(
                CopySource=copy_source, Bucket=self.config.bucket_name, Key=dest_key
            )

            logger.info(
                f"Copied {source_bucket}/{source_key} to {self.config.bucket_name}/{dest_key}"
            )

            return True

        except Exception as e:
            logger.error(f"Failed to copy object: {e}")

            return False

    def get_bucket_size(self) -> tuple[int, int]:
        """Get bucket size and object count.





        Returns:


            Tuple of (total_size_bytes, object_count)


        """

        try:
            objects = self.list_objects()

            total_size = sum(obj.size for obj in objects)

            object_count = len(objects)

            return total_size, object_count

        except Exception as e:
            logger.error(f"Failed to get bucket size: {e}")

            return 0, 0

    def cleanup_old_objects(self, max_age_days: int, prefix: str = "") -> int:
        """Remove objects older than specified age.





        Args:


            max_age_days: Maximum age in days


            prefix: Object key prefix filter





        Returns:


            Number of objects deleted


        """

        cutoff_date = datetime.now() - timedelta(days=max_age_days)

        deleted_count = 0

        try:
            objects = self.list_objects(prefix=prefix)

            for obj in objects:
                if obj.last_modified < cutoff_date:
                    if self.delete_object(obj.key):
                        deleted_count += 1

            logger.info(f"Cleaned up {deleted_count} old objects")

        except Exception as e:
            logger.error(f"Failed to cleanup old objects: {e}")

        return deleted_count


# Convenience functions for quick S3 operations


def create_s3_storage(
    access_key: str,
    secret_key: str,
    bucket_name: str,
    endpoint_url: str | None = None,
    region: str = "us-east-1",
) -> S3Storage:
    """Create S3 storage with basic configuration.





    Args:


        access_key: S3 access key


        secret_key: S3 secret key


        bucket_name: Bucket name


        endpoint_url: S3 endpoint URL (None for AWS)


        region: AWS region





    Returns:


        S3Storage instance


    """

    config = S3Config(
        endpoint_url=endpoint_url,
        access_key=access_key,
        secret_key=secret_key,
        region=region,
        bucket_name=bucket_name,
    )

    return S3Storage(config)


def quick_upload_file(
    local_path: str | Path,
    key: str,
    access_key: str,
    secret_key: str,
    bucket_name: str,
    endpoint_url: str | None = None,
) -> S3Object | None:
    """Quick file upload to S3.





    Args:


        local_path: Local file to upload


        key: S3 object key


        access_key: S3 access key


        secret_key: S3 secret key


        bucket_name: Bucket name


        endpoint_url: S3 endpoint URL





    Returns:


        S3Object if successful


    """

    storage = create_s3_storage(
        access_key=access_key,
        secret_key=secret_key,
        bucket_name=bucket_name,
        endpoint_url=endpoint_url,
    )

    # Ensure bucket exists

    storage.create_bucket()

    return storage.upload_file(local_path, key)
