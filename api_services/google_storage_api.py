from constant_variables.configs import KEY_FILE_LOCATION
from google.cloud import storage


class GoogleStorageAPI:
    def __init__(self) -> None:
        pass

    def upload_blob(self, bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"
        # The path to your file to upload
        # source_file_name = "local/path/to/file"
        # The ID of your GCS object
        # destination_blob_name = "storage-object-name"

        storage_client = storage.Client.from_service_account_json(KEY_FILE_LOCATION)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Optional: set a generation-match precondition to avoid potential race conditions
        # and data corruptions. The request to upload is aborted if the object's
        # generation number does not match your precondition. For a destination
        # object that does not yet exist, set the if_generation_match precondition to 0.
        # If the destination object already exists in your bucket, set instead a
        # generation-match precondition using its generation number.
        generation_match_precondition = blob.generation if blob.exists() else 0

        blob.upload_from_filename(
            source_file_name, if_generation_match=generation_match_precondition
        )

        gs_file_path = f"gs://{bucket_name}/{destination_blob_name}"

        return gs_file_path

    def delete_blob(self, bucket_name, blob_name):
        """Deletes a blob from the bucket."""
        # bucket_name = "your-bucket-name"
        # blob_name = "your-object-name"

        storage_client = storage.Client.from_service_account_json(KEY_FILE_LOCATION)

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        generation_match_precondition = None

        # Optional: set a generation-match precondition to avoid potential race conditions
        # and data corruptions. The request to delete is aborted if the object's
        # generation number does not match your precondition.
        blob.reload()  # Fetch blob metadata to use in generation_match_precondition.
        generation_match_precondition = blob.generation

        blob.delete(if_generation_match=generation_match_precondition)

        return f"Blob {blob_name} deleted."
