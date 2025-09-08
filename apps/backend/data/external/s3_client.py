"""S3 client for cloud storage operations."""

from __future__ import annotations

import io
import logging
from datetime import UTC, datetime
from typing import Any

try:  # Optional dependency
    import boto3  # type: ignore[import-not-found]
    from botocore.exceptions import (
        BotoCoreError,  # type: ignore[import-not-found]
        ClientError,
    )

    _HAS_BOTO3 = True


except Exception:  # pragma: no cover - optional import path
    boto3 = None  # type: ignore[assignment]

    # Fallback exception types if botocore is unavailable

    class BotoCoreError(Exception):
        pass

    class ClientError(Exception):
        pass

    _HAS_BOTO3 = False


logger = logging.getLogger(__name__)


class S3Client:
    """Client for Amazon S3 storage operations."""
import Exception
import ImportError
import RuntimeError
import access_key
import bool
import bucket_name
import bytes
import content_type
import dest_key
import dict
import e
import endpoint_url
import expiration
import file_path
import getattr
import http_method
import int
import isinstance
import key
import len
import list
import max_keys
import metadata
import obj
import prefix
import region
import secret_key
import self
import source_key
import str

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        region: str = "us-east-1",
        endpoint_url: str | None = None,
    ):
        """Initialize the S3 client.





        Args:


            access_key: AWS access key ID


            secret_key: AWS secret access key


            bucket_name: S3 bucket name


            region: AWS region


            endpoint_url: Optional custom endpoint URL (for S3-compatible services)


        """

        self.access_key = access_key

        self.secret_key = secret_key

        self.bucket_name = bucket_name

        self.region = region

        self.endpoint_url = endpoint_url

        if not _HAS_BOTO3:
            raise ImportError(
                "boto3 is required for S3Client but is not installed. Add 'boto3' to your dependencies or avoid using S3Client."
            )

        # Initialize S3 client

        self._client = boto3.client(  # type: ignore[union-attr]
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
            endpoint_url=endpoint_url,
        )

    async def upload_file(
        self,
        file_path: str,
        key: str,
        metadata: dict[str, str] | None = None,
        content_type: str | None = None,
    ) -> dict[str, Any]:
        """Upload a file to S3.





        Args:


            file_path: Local file path


            key: S3 object key


            metadata: Optional metadata


            content_type: Optional content type





        Returns:


            Dict containing upload results





        Raises:


            RuntimeError: If upload fails


        """

        try:
            extra_args = {}

            if metadata:
                extra_args["Metadata"] = metadata

            if content_type:
                extra_args["ContentType"] = content_type

            # Upload file

            self._client.upload_file(
                file_path, self.bucket_name, key, ExtraArgs=extra_args
            )

            logger.info(
                f"Successfully uploaded {file_path} to s3://{self.bucket_name}/{key}"
            )

            return {
                "success": True,
                "bucket": self.bucket_name,
                "key": key,
                "url": f"s3://{self.bucket_name}/{key}",
                "uploaded_at": datetime.now(UTC).isoformat(),
            }

        except (BotoCoreError, ClientError) as e:
            logger.error(f"Failed to upload file {file_path}: {e}")

            raise RuntimeError(f"S3 upload failed: {e}") from e

    async def upload_data(
        self,
        data: str | bytes,
        key: str,
        metadata: dict[str, str] | None = None,
        content_type: str | None = None,
    ) -> dict[str, Any]:
        """Upload data directly to S3.





        Args:


            data: Data to upload (string or bytes)


            key: S3 object key


            metadata: Optional metadata


            content_type: Optional content type





        Returns:


            Dict containing upload results


        """

        try:
            # Convert string to bytes if needed
            data_bytes = data.encode("utf-8") if isinstance(data, str) else data

            extra_args = {}

            if metadata:
                extra_args["Metadata"] = metadata

            if content_type:
                extra_args["ContentType"] = content_type

            # Upload data

            self._client.upload_fileobj(
                io.BytesIO(data_bytes), self.bucket_name, key, ExtraArgs=extra_args
            )

            logger.info(f"Successfully uploaded data to s3://{self.bucket_name}/{key}")

            return {
                "success": True,
                "bucket": self.bucket_name,
                "key": key,
                "size_bytes": len(data_bytes),
                "url": f"s3://{self.bucket_name}/{key}",
                "uploaded_at": datetime.now(UTC).isoformat(),
            }

        except (BotoCoreError, ClientError) as e:
            logger.error(f"Failed to upload data to {key}: {e}")

            raise RuntimeError(f"S3 data upload failed: {e}") from e

    async def download_file(self, key: str, file_path: str) -> dict[str, Any]:
        """Download a file from S3.





        Args:


            key: S3 object key


            file_path: Local file path to save





        Returns:


            Dict containing download results


        """

        try:
            self._client.download_file(self.bucket_name, key, file_path)

            logger.info(
                f"Successfully downloaded s3://{self.bucket_name}/{key} to {file_path}"
            )

            return {
                "success": True,
                "bucket": self.bucket_name,
                "key": key,
                "file_path": file_path,
                "downloaded_at": datetime.now(UTC).isoformat(),
            }

        except (BotoCoreError, ClientError) as e:
            logger.error(f"Failed to download file {key}: {e}")

            raise RuntimeError(f"S3 download failed: {e}") from e

    async def download_data(self, key: str) -> bytes:
        """Download data from S3 as bytes.





        Args:


            key: S3 object key





        Returns:


            Downloaded data as bytes


        """

        try:
            response = self._client.get_object(Bucket=self.bucket_name, Key=key)

            data = response["Body"].read()

            logger.info(
                f"Successfully downloaded data from s3://{self.bucket_name}/{key}"
            )

            return data

        except (BotoCoreError, ClientError) as e:
            logger.error(f"Failed to download data from {key}: {e}")

            raise RuntimeError(f"S3 data download failed: {e}") from e

    async def delete_object(self, key: str) -> dict[str, Any]:
        """Delete an object from S3.





        Args:


            key: S3 object key





        Returns:


            Dict containing deletion results


        """

        try:
            self._client.delete_object(Bucket=self.bucket_name, Key=key)

            logger.info(f"Successfully deleted s3://{self.bucket_name}/{key}")

            return {
                "success": True,
                "bucket": self.bucket_name,
                "key": key,
                "deleted_at": datetime.now(UTC).isoformat(),
            }

        except (BotoCoreError, ClientError) as e:
            logger.error(f"Failed to delete object {key}: {e}")

            raise RuntimeError(f"S3 deletion failed: {e}") from e

    async def list_objects(
        self, prefix: str = "", max_keys: int = 1000
    ) -> list[dict[str, Any]]:
        """List objects in the S3 bucket.





        Args:


            prefix: Optional prefix to filter objects


            max_keys: Maximum number of objects to return





        Returns:


            List of object information dictionaries


        """

        try:
            response = self._client.list_objects_v2(
                Bucket=self.bucket_name, Prefix=prefix, MaxKeys=max_keys
            )

            objects = []

            for obj in response.get("Contents", []):
                objects.append(
                    {
                        "key": obj["Key"],
                        "size": obj["Size"],
                        "last_modified": obj["LastModified"].isoformat(),
                        "etag": obj["ETag"].strip('"'),
                        "storage_class": obj.get("StorageClass", "STANDARD"),
                    }
                )

            logger.info(f"Listed {len(objects)} objects with prefix '{prefix}'")

            return objects

        except (BotoCoreError, ClientError) as e:
            logger.error(f"Failed to list objects: {e}")

            raise RuntimeError(f"S3 list objects failed: {e}") from e

    async def object_exists(self, key: str) -> bool:
        """Check if an object exists in S3.





        Args:


            key: S3 object key





        Returns:


            True if object exists, False otherwise


        """

        try:
            self._client.head_object(Bucket=self.bucket_name, Key=key)

            return True

        except ClientError as e:
            # Some type checkers don't know about ClientError.response, access defensively
            resp = getattr(e, "response", None)
            code = None
            if isinstance(resp, dict):
                err = resp.get("Error")
                if isinstance(err, dict):
                    code = err.get("Code")
            if code == "404":
                return False
            logger.error(f"Error checking object existence for {key}: {e}")
            raise RuntimeError(f"S3 object check failed: {e}") from e

    async def get_object_metadata(self, key: str) -> dict[str, Any]:
        """Get metadata for an S3 object.





        Args:


            key: S3 object key





        Returns:


            Dict containing object metadata


        """

        try:
            response = self._client.head_object(Bucket=self.bucket_name, Key=key)

            return {
                "key": key,
                "size": response["ContentLength"],
                "last_modified": response["LastModified"].isoformat(),
                "etag": response["ETag"].strip('"'),
                "content_type": response.get("ContentType", "binary/octet-stream"),
                "metadata": response.get("Metadata", {}),
                "storage_class": response.get("StorageClass", "STANDARD"),
            }

        except (BotoCoreError, ClientError) as e:
            logger.error(f"Failed to get metadata for {key}: {e}")

            raise RuntimeError(f"S3 metadata retrieval failed: {e}") from e

    async def create_presigned_url(
        self, key: str, expiration: int = 3600, http_method: str = "GET"
    ) -> str:
        """Create a presigned URL for an S3 object.





        Args:


            key: S3 object key


            expiration: URL expiration time in seconds


            http_method: HTTP method (GET, PUT, etc.)





        Returns:


            Presigned URL string


        """

        try:
            client_method = "get_object" if http_method == "GET" else "put_object"

            url = self._client.generate_presigned_url(
                client_method,
                Params={"Bucket": self.bucket_name, "Key": key},
                ExpiresIn=expiration,
            )

            logger.info(f"Generated presigned URL for {key} (expires in {expiration}s)")

            return url

        except (BotoCoreError, ClientError) as e:
            logger.error(f"Failed to create presigned URL for {key}: {e}")

            raise RuntimeError(f"Presigned URL creation failed: {e}") from e

    async def copy_object(
        self, source_key: str, dest_key: str, source_bucket: str | None = None
    ) -> dict[str, Any]:
        """Copy an object within S3.





        Args:


            source_key: Source object key


            dest_key: Destination object key


            source_bucket: Source bucket (defaults to current bucket)





        Returns:


            Dict containing copy results


        """

        try:
            if source_bucket is None:
                source_bucket = self.bucket_name

            copy_source = {"Bucket": source_bucket, "Key": source_key}

            self._client.copy_object(
                CopySource=copy_source, Bucket=self.bucket_name, Key=dest_key
            )

            logger.info(
                f"Successfully copied {source_bucket}/{source_key} to {self.bucket_name}/{dest_key}"
            )

            return {
                "success": True,
                "source_bucket": source_bucket,
                "source_key": source_key,
                "dest_bucket": self.bucket_name,
                "dest_key": dest_key,
                "copied_at": datetime.now(UTC).isoformat(),
            }

        except (BotoCoreError, ClientError) as e:
            logger.error(f"Failed to copy object {source_key}: {e}")

            raise RuntimeError(f"S3 copy failed: {e}") from e

    async def get_bucket_info(self) -> dict[str, Any]:
        """Get information about the S3 bucket.





        Returns:


            Dict containing bucket information


        """

        try:
            # Get bucket location

            location_response = self._client.get_bucket_location(
                Bucket=self.bucket_name
            )

            location = location_response.get("LocationConstraint") or "us-east-1"

            # Get bucket versioning

            try:
                versioning_response = self._client.get_bucket_versioning(
                    Bucket=self.bucket_name
                )

                versioning_status = versioning_response.get("Status", "Disabled")

            except ClientError:
                versioning_status = "Unknown"

            return {
                "bucket_name": self.bucket_name,
                "region": location,
                "versioning": versioning_status,
                "endpoint": self.endpoint_url or "https://s3.amazonaws.com",
            }

        except (BotoCoreError, ClientError) as e:
            logger.error(f"Failed to get bucket info: {e}")

            raise RuntimeError(f"Bucket info retrieval failed: {e}") from e

    async def health_check(self) -> dict[str, Any]:
        """Perform a health check on the S3 connection.





        Returns:


            Dict containing health check results


        """

        try:
            # Try to list bucket (this tests connectivity and permissions)

            self._client.list_objects_v2(Bucket=self.bucket_name, MaxKeys=1)

            bucket_info = await self.get_bucket_info()

            return {
                "status": "healthy",
                "bucket_info": bucket_info,
                "timestamp": datetime.now(UTC).isoformat(),
            }

        except Exception as e:
            logger.error(f"S3 health check failed: {e}")

            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            }

    def __repr__(self) -> str:
        """String representation of the S3 client."""

        return f"S3Client(bucket='{self.bucket_name}', region='{self.region}')"
