from decouple import config

KEY_FILE_LOCATION = config("KEY_FILE_LOCATION")
BUCKET_NAME = config("BUCKET_NAME")
DATABASE_URL = config("DATABASE_URL")

DOC_EXTENSIONS = [".txt"]
