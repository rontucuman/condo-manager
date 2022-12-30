import os

from azure.storage.blob import BlobServiceClient, ContentSettings, BlobType
from django.conf import settings


class AzureBlobManager:
    connection_string = settings.AZURE_STORAGE_CONN_STR
    container_name = settings.AZURE_STORAGE_CONTAINER

    def upload_file(self, filename, src_folder, content_type):
        blob_service_client = BlobServiceClient.from_connection_string(conn_str=self.connection_string)
        try:
            filepath = os.path.join(src_folder, filename)
            if os.path.exists(filepath):
                blob_client = blob_service_client.get_blob_client(container=self.container_name, blob=filename)
                with open(file=filepath, mode='rb') as file:
                    blob_client.upload_blob(
                        data=file,
                        blob_type=BlobType.BLOCKBLOB,
                        content_settings=ContentSettings(content_type=content_type))
                return True
            return False
        except:
            return False

    def download_file(self, filename, dest_folder):
        blob_service_client = BlobServiceClient.from_connection_string(conn_str=settings.AZURE_STORAGE_CONN_STR)
        try:
            blob_client = blob_service_client.get_blob_client(container=self.container_name, blob=filename)
            filepath = os.path.join(dest_folder, filename)

            if blob_client.exists():
                with open(filepath, 'wb') as file:
                    download_stream = blob_client.download_blob()
                    file.write(download_stream.readall())
                return True

            return False
        except:
            return False
