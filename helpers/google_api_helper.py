class GoogleApiHelper:
    def __init__(self) -> None:
        pass

    def get_blob_name(self, object_path):
        """
        Extracts the blob name from the provided Google Cloud Storage object path.

        Args:
            object_path (str): The full object path in the format 'gs://bucket-name/blob-name'.

        Returns:
            str: The blob name.
        """
        # Remove the 'gs://' prefix
        object_path = object_path.replace("gs://", "")

        # Split the path into bucket name and blob name
        parts = object_path.split("/", 1)

        if len(parts) < 2:
            raise ValueError(
                "Invalid object path format. Expected 'gs://bucket-name/blob-name'."
            )

        blob_name = parts[1]

        return blob_name
