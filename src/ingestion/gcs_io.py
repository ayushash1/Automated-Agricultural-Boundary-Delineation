def get_gcs_files(bucket_name, prefix):
    """
    Retrieves a list of file names from a Google Cloud Storage bucket.
    """
    from google.cloud import storage

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)

    files = []
    for blob in blobs:
        files.append(blob.name)

    return files

get_gcs_files('boundary-deliation', 'data/')