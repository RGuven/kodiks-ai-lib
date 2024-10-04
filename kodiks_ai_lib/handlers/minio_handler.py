import json
import os
import time
from io import BytesIO
from pathlib import Path

from loguru import logger
from minio import Minio, S3Error


class MinioService:
    def __init__(self, endpoint, access_key, secret_key, secure=True):
        """
        Initializes a connection to the MinIO server.

        :param endpoint: MinIO server endpoint (e.g., "localhost:9000")
        :param access_key: Access key for MinIO
        :param secret_key: Secret key for MinIO
        :param secure: Use secure connection (HTTPS) if True, HTTP otherwise
        """
        try:
            self.client = Minio(endpoint=endpoint, access_key=access_key, secret_key=secret_key, secure=secure)
            logger.info(f"🔧 Connected to MinIO server: {endpoint}")
        except Exception as e:
            logger.error(f"❌ Failed to connect to MinIO server: {e} - {endpoint}")
            return False, f"Connection error: {e}"

    def download_files(self, bucket_name, prefix, local_download_path):
        """
        Downloads files from a specified bucket and folder in MinIO, saving them to a local folder.

        :param bucket_name: Name of the bucket in MinIO
        :param prefix: Path to the files inside the bucket
        :param local_download_path: Local folder where the files will be saved
        :return: Tuple (success: bool, message: str or list) with the result status and message
        """
        logger.info("*" * 70)

        # Create the local folder if it does not exist
        if not os.path.exists(local_download_path):
            os.makedirs(local_download_path)
            logger.info(f"📁 Created directory: {local_download_path}")

        downloaded_files = []
        try:
            tic = time.time()
            # List all objects in the specified bucket path (prefix)
            objects = self.client.list_objects(bucket_name, prefix=prefix, recursive=True)

            for obj in objects:
                file_path = os.path.join(local_download_path, os.path.basename(obj.object_name))

                # Skip downloading if the file already exists locally
                if os.path.exists(file_path):
                    logger.info(f"⚠️ File already exists, skipping download: {file_path}")
                    continue

                logger.info(f"📥 Downloading: {obj.object_name}...")
                self.client.fget_object(bucket_name, obj.object_name, file_path)
                logger.info(f"✅ Downloaded and saved to: {file_path}")
                downloaded_files.append(file_path)

            toc = time.time()
            logger.info(f"⏱️ Elapsed Time: {toc - tic:.2f} seconds")
            logger.success("✅Download completed")
            logger.info("*" * 70)

            return True, downloaded_files

        except S3Error as e:
            logger.error(f"MinIO Error: {e}")
            return False, f"MinIO Error: {e}"

    def upload_file(self, bucket_name, prefix, local_upload_file_path):
        """
        Uploads a local file to a specified MinIO bucket.

        :param bucket_name: Name of the bucket in MinIO
        :param prefix: Path inside the bucket where the file will be uploaded
        :param local_upload_file_path: Local path to the file to be uploaded
        :return: Tuple (success: bool, message: str) indicating upload result
        """
        logger.info("*" * 70)

        # Check if the local file exists before uploading
        if not os.path.exists(local_upload_file_path):
            logger.error(f"📁 File not found: {local_upload_file_path}")
            return False, f"File not found: {local_upload_file_path}"

        try:
            tic = time.time()
            file = Path(local_upload_file_path)
            object_name = os.path.join(prefix, file.name)

            logger.info(f"⬆️ Uploading: {file.name}...")
            self.client.fput_object(bucket_name, object_name, local_upload_file_path)
            logger.info(f"✅ Uploaded: {file.name}")

            toc = time.time()
            logger.info(f"⏱️ Elapsed Time: {toc - tic:.2f} seconds")
            logger.success("✔️ Upload completed.")
            logger.info("*" * 70)

            return True, f"Successfully uploaded {file.name}"

        except S3Error as e:
            logger.error(f"MinIO Upload Error: {e}")
            return False, f"MinIO Upload Error: {e}"

    def write_file(self, bucket_name, object_name, content, content_type=None):
        """
        Writes content (text, JSON, or binary) to a specified MinIO bucket.

        :param object_name: Full name of the object in the bucket (path and file name)
        :param content: Content to be written (can be text, JSON, or binary data)
        :param content_type: MIME type of the content (e.g., 'text/plain', 'application/json', 'image/jpeg')
        :return: Tuple (success: bool, message: str) indicating the write result
        """
        logger.info("*" * 70)

        try:
            tic = time.time()

            # Automatically determine content type if not provided
            if content_type is None:
                if isinstance(content, dict):
                    content_type = "application/json"
                    content = json.dumps(content)  # Convert dict to JSON string
                    content = BytesIO(content.encode("utf-8"))  # Convert to BytesIO for upload
                elif isinstance(content, str):
                    content_type = "text/plain"
                    content = BytesIO(content.encode("utf-8"))  # Convert text to BytesIO
                elif isinstance(content, bytes):
                    content_type = "application/octet-stream"
                    content = BytesIO(content)  # Treat as binary data

            # Determine content length for upload
            content_length = len(content.getvalue())

            # Upload content to MinIO
            logger.info(f"⬆️ Uploading: {object_name}...")
            self.client.put_object(bucket_name, object_name, content, content_length, content_type=content_type)
            logger.info(f"✅ Uploaded: {object_name}")

            toc = time.time()
            logger.info(f"⏱️ Elapsed Time: {toc - tic:.2f} seconds")
            logger.success("✔️ Upload completed.")
            logger.info("*" * 70)

            return True, f"Successfully wrote {object_name}"

        except S3Error as e:
            logger.error(f"MinIO Upload Error: {e}")
            return False, f"MinIO Upload Error: {e}"
